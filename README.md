# Event App

This project is a simple event manager. Organize your events effortlessly and stay updated with the latest weather forecasts

## Main Technologies Used

- Python
- Django
- Pydantic
- PostgreSQL
- Weather API (https://api-ninjas.com/api/weather)
- Docker
- Prometheus
- Grafana

## Deploying the Project

### Requirements
- Docker and Docker Compose installed
- GNU Make (https://www.gnu.org/software/make/)

### Demo:
<a href="https://youtu.be/gLDd0n_yaUc">
    <img src="https://nihot.nl/wp/wp-content/uploads/2017/02/YouTube-click-here.png" width="600" alt="Alt text for your video">
</a>

### Instructions:
1. Clone the repository
   ```bash
   git clone https://github.com/kirillovme/event_app.git
   ```
2. Rename `.env.example` to `.env` and complete fields
   - You will need to go to [https://api-ninjas.com/api/weather](https://api-ninjas.com/api/weather) and get your API key
   - Fill WEATHER_API_TOKEN with your api key
   - After go to [https://djecrety.ir/](https://djecrety.ir/) and get you Django secret key
   - Fill SECRET_KEY with generated secret key
3. (If needed) Open entrypoint.sh from src and change coding of the file from CRLF to LF to prevent errors.
4. Run containers
   ```bash
   make up-d
   ```
5. Run tests
   ```bash
   make test
   ```
