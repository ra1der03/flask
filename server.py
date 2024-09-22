from datetime import datetime
import pydantic
from aiohttp import web
from sqlalchemy.exc import IntegrityError
import json
from model.models import Base, Session, Advertisement, engine
from model.schema import CreateAdvertisement, Schema, UpdateAdvertisement

app = web.Application()


async def orm_context(app):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request.session = session
        response = await handler(request)
        return response


app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)


def get_http_error(error_class, msg):
    return error_class(text=json.dumps({'error': msg}), content_type='application/json')


def validate(schema_cls: Schema, json_data: dict):
    try:
        return schema_cls(**json_data).dict(exclude_unset=True)
    except pydantic.ValidationError as err:
        error = err.errors()[0]
        error.pop("ctx", None)
        raise get_http_error(pydantic.ValidationError, error)


async def get_advertisement(session: Session, advertisement_id: int):
    advertisement = await session.get(Advertisement, advertisement_id)
    if advertisement is None:
        raise get_http_error(web.HTTPNotFound, "advertisement not found")
    return advertisement


async def add_advertisement(session: Session, advertisement: Advertisement):
    try:
        session.add(advertisement)
        await session.commit()
        return advertisement
    except IntegrityError:
        exc = get_http_error(web.HTTPConflict, 'advertisement already exists')
        raise exc


class AdvertisementView(web.View):

    @property
    def session(self) -> Session:
        return self.request.session

    @property
    def advertisement_id(self) -> int:
        return int(self.request.match_info["advertisement_id"])

    async def get(self):
        advertisement = await get_advertisement(self.session, self.advertisement_id)
        return web.json_response({
            'id': advertisement.id,
            'name': advertisement.name,
            'description': advertisement.description,
            'owner': advertisement.owner,
            'registration_time': datetime.fromtimestamp(advertisement.registration_time.timestamp()
                                                        ).strftime('%Y-%m-%d:%H-%M')
        })

    async def post(self):
        json_data = validate(CreateAdvertisement, await self.request.json())
        advertisement = Advertisement(**json_data)
        advertisement = await add_advertisement(self.session, advertisement)
        return web.json_response({'id': advertisement.id})

    async def patch(self):
        advertisement = await get_advertisement(self.session, self.advertisement_id)
        json_data = validate(UpdateAdvertisement, await self.request.json())
        for field, value in json_data.items():
            setattr(advertisement, field, value)
        await add_advertisement(self.session, advertisement)
        return web.json_response({'id': advertisement.id})

    async def delete(self):
        advertisement = await get_advertisement(self.session, self.advertisement_id)
        await self.session.delete(advertisement)
        await self.session.commit()
        return web.json_response({"status": "deleted"})


app.add_routes(
    [
        web.post("/advertisement", AdvertisementView),
        web.get(r"/advertisement/{advertisement_id:\d+}", AdvertisementView),
        web.patch(r"/advertisement/{advertisement_id:\d+}", AdvertisementView),
        web.delete(r"/advertisement/{advertisement_id:\d+}", AdvertisementView),
    ]
)
web.run_app(app)
