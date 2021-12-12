<img src=".docs/logo.png" width="64px" align="right"/>

# Fast App - API

![License](https://img.shields.io/github/license/avcaliani/fast-app?logo=apache&color=lightseagreen)
![#](https://img.shields.io/badge/python-3.10.x-yellow.svg)

## Quick Start

Create your Python virtual environment...

```bash
python -m venv .venv \
    && source .venv/bin/activate \
    && pip install --upgrade pip \
    && poetry install
```

Then, create a Dynaconf secrets file as follows.

```bash
echo "
[default]
TOKEN_SECRET_KEY = '$(openssl rand -hex 32)'

[dev]
SECRET = '🚀'

[prod]
SECRET = '🤫'
" > .secrets.toml
```

Finally, start the API server.

> `APP_ENV` is an environment variable used by Dynaconf to indicate which profile should be used.

```bash
APP_ENV=dev uvicorn main:app --reload
```

After executing the previous command you are ready to access the API resources.

- API Home: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

![home](.docs/home.png)

#### Example

```bash
curl -X 'GET' 'http://127.0.0.1:8000/emoji'
# {"lucky_emojis":["🫐","🍈","🍊","🍋","🥭","🍐"],"secret":"🚀","consulted_at":"2021-10-22T11:36:48.533441"}
```

### References

- [Fast API: docs](https://fastapi.tiangolo.com/)
- [pydantic: docs](https://pydantic-docs.helpmanual.io/)
- [Icon made by Strokeicon from IconFinder](https://www.iconfinder.com/icons/2191531/best_fast_flash_good_light_speed_icon)

> 💡 Fast API has an awesome documentation!
