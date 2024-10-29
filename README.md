[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![Discord][discord-shield]][discord-url]
[![Docker Pulls][docker-shield]][docker-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Matt0550/MIUR-OpenData-rest-api">
    <img src="https://raw.githubusercontent.com/Matt0550/public-gaac/main/uploads/logo-MIM-schools-rest-api-2.png" alt="Logo" height="200">
  </a>

  <h3 align="center">MIUR/MIM Open-Data REST API</h3>

  <p align="center">
    An unofficial REST API for the MIUR/MIM Open-Data. Using FastAPI and SPARQL.
    <br />
    <br />
    <a href="https://github.com/Matt0550/MIUR-OpenData-rest-api/issues">Report Bug</a>
    ·
    <a href="https://github.com/Matt0550/MIUR-OpenData-rest-api/issues">Request Feature</a>
  </p>
</div>

All the data used in this project is owned by the respective owners and is used for educational purposes only. The data is taken from the official [MIUR/MIM Open-Data website](https://dati.istruzione.it/opendata/).


## Features

- Get and query all the data about the schools in Italy
- Cache the data to reduce the number of requests to the MIUR/MIM Open-Data website


## API Endpoints
> [!TIP]
> The API is self-documented. You can access the Swagger UI at `/docs` and the ReDoc UI at `/redoc`.

### Base URL
```
  https://miur-api.cloud.matteosillitti.it/v1/
```

### Schools
- `/schools` - Get all the schools or filter them by SchoolBase model.

#### Query parameters
- `limit` - Limit the number of results (default: 50, max: 1500)
- `exclude_par` - Exclude private schools (default: false)
- `exclude_aut` - Exclude autonomous schools like Aosta, Trento e Bolzano (default: false)

##### Body (SchoolBase model)
```json
{
  "school_year": 202425,
  "geographic_area": "string",
  "region": "string",
  "province": "string",
  "school_code": "string",
  "school_name": "string",
  "school_address": "string",
  "school_postal_code": "string",
  "school_city_code": "string",
  "city_description": "string",
  "education_type_description": "string",
  "school_email_address": "string",
  "school_certified_email_address": "string",
  "school_website": "string",
}
```

#### Response
```json
{
    "details": {
        "schools": [
            {
                "school_year": 202425,
                "geographic_area": "ISOLE",
                "region": "SICILIA",
                "province": "CALTANISSETTA",
                "school_code": "CLTD090005",
                "school_name": "\"M. RAPISARDI\" - CALTANISSETT",
                "school_address": "VIALE REGINA MARGHERITA",
                "school_postal_code": "93100",
                "school_city_code": "B429",
                "city_description": "CALTANISSETTA",
                "education_type_description": "ISTITUTO TECNICO COMMERCIALE",
                "school_email_address": "CLTD090005@istruzione.it",
                "school_certified_email_address": "Non Disponibile",
                "school_website": ""
            }
        ],
        "total": 
    },
    "success": true,
    "status_code": 200
}
```

## Cache
The API uses a cache system to reduce the number of requests to the MIUR/MIM Open-Data website. The cache expiration time is set to 1 hour by default. You can change it using the `CACHE_EXPIRE` environment variable. The cache is stored in memory and is not persistent. Soon I will add the possibility to use Redis as a cache.

## Public instance of the API
An instance of the API is available at https://miur-api.cloud.matteosillitti.it/

Limited to 20 requests per day (2 requests per minute). If you need more requests, contact me.

## Environment Variables
| Variable | Description | Default |
| :--- | :--- | :--- |
| `PUID` | User ID (docker) | `1000` |
| `PGID` | Group ID (docker) | `1000` |
| `DOMAIN` | Domain of the API | `localhost` |
| `PORT` | Port of the API | `5000` |
| `CACHE_EXPIRE` | Cache expiration time in seconds | `3600` (1 hour) |

## Installation - Using Docker Compose (recommended)
Clone the project

```yml
version: '3'

services:
  miur_opendata_rest_api:
    image: matt0550/miur-opendata-rest-api
    environment:
      - PUID=1000
      - PGID=1000
    ports:
      - 5000:5000
    restart: unless-stopped
```

Run the container with `docker-compose up -d`

## Installation - Using Docker Run
Pull the image

```bash
  docker run -d -p 5000:5000 -e PUID=1000 -e PGID=1000 matt0550/miur-opendata-rest-api
```

## Installation - Self-Host or docker build

Clone the project

```bash
  git clone https://github.com/Matt0550/MIUR-OpenData-rest-api
```

Go to the project directory

```bash
  cd MIUR-OpenData-rest-api-master
```

OPTIONAL: use docker to build the image

```bash
  docker build -t MIUR-OpenData-rest-api .
```

If you don't want to use docker, skip this step.
Else, change the `image` in `docker-compose.yml` with the image name you used.
Run the container with `docker-compose up -d`

Install dependencies

```bash
  poetry install
```

Start the REST API (after setting the environment variables)

```bash
  cd app
  uvicorn main:app
```

## Help - feedback
You can contact me on:

Discord: https://go.matteosillitti.it/discord

Telegram: https://go.matteosillitti.it/telegram

Mail: <a href="mailto:mail@matteosillitti.it">me@matteosillitti.it</a>

## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)

## Support me

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/matt05)

[![buy-me-a-coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/Matt0550)

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://paypal.me/sillittimatteo)

[contributors-shield]: https://img.shields.io/github/contributors/Matt0550/MIUR-OpenData-rest-api.svg?style=for-the-badge
[contributors-url]: https://github.com/Matt0550/MIUR-OpenData-rest-api/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Matt0550/MIUR-OpenData-rest-api.svg?style=for-the-badge
[forks-url]: https://github.com/Matt0550/MIUR-OpenData-rest-api/network/members
[stars-shield]: https://img.shields.io/github/stars/Matt0550/MIUR-OpenData-rest-api.svg?style=for-the-badge
[stars-url]: https://github.com/Matt0550/MIUR-OpenData-rest-api/stargazers
[issues-shield]: https://img.shields.io/github/issues/Matt0550/MIUR-OpenData-rest-api.svg?style=for-the-badge
[issues-url]: https://github.com/Matt0550/MIUR-OpenData-rest-api/issues
[license-shield]: https://img.shields.io/github/license/Matt0550/MIUR-OpenData-rest-api.svg?style=for-the-badge
[license-url]: https://github.com/Matt0550/MIUR-OpenData-rest-api/blob/master/LICENSE
[discord-shield]: https://img.shields.io/discord/828990499507404820?style=for-the-badge
[discord-url]: https://go.matteosillitti.it/discord
[docker-shield]: https://img.shields.io/docker/pulls/matt0550/miur-opendata-rest-api?style=for-the-badge
[docker-url]: https://hub.docker.com/r/matt0550/miur-opendata-rest-api
