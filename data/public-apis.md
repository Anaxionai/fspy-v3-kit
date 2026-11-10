# Free public APIs that need no key

Each API below answers an HTTP `GET` request with JSON, and needs no account and no API key.
Every example address was checked on 10 November 2026 and returned status 200 with JSON.
Open an address in your browser first, then call it from Git Bash with `curl`.

## How to call one from Git Bash

```bash
curl -si "https://api.open-meteo.com/v1/forecast?latitude=18.52&longitude=73.86&current=temperature_2m" | head -n 12
curl -s "https://api.open-meteo.com/v1/forecast?latitude=18.52&longitude=73.86&current=temperature_2m" | uv run python -m json.tool
```

- `-i` shows the status line and the headers. `-s` hides the progress bar.
- Keep the quotes around every address: they protect `?` and `&` from Git Bash.
- `uv run python -m json.tool` shows the JSON one field per line.
- In PowerShell, `curl` is a different command. Type `curl.exe` there instead.

## The list

| API | What it gives | Example address |
|---|---|---|
| **Open-Meteo** | Weather now and forecasts for any place | `https://api.open-meteo.com/v1/forecast?latitude=18.52&longitude=73.86&current=temperature_2m,wind_speed_10m&timezone=Asia%2FKolkata` |
| **JSONPlaceholder** | Fake posts, users and to-do items for practice | `https://jsonplaceholder.typicode.com/todos/1` |
| **PokeAPI** | Pokémon and their types, moves and abilities | `https://pokeapi.co/api/v2/pokemon/pikachu` |
| **Open Library** | Books and authors, from the Internet Archive | `https://openlibrary.org/search.json?title=wings+of+fire&author=kalam&fields=title,author_name,first_publish_year&limit=3` |
| **World Bank** | Countries: region, capital, income level | `https://api.worldbank.org/v2/country/IND?format=json` |
| **Frankfurter** | Currency exchange rates from the European Central Bank | `https://api.frankfurter.dev/v1/latest?base=USD&symbols=INR` |
| **India Post PIN codes** | The post offices for an Indian PIN code | `https://api.postalpincode.in/pincode/411001` |
| **Wikipedia** | A short summary of a Wikipedia article | `https://en.wikipedia.org/api/rest_v1/page/summary/Indian_Railways` |
| **GitHub** | A GitHub user's public profile | `https://api.github.com/users/octocat` |
| **Sunrise Sunset** | Sunrise and sunset times for a place and a date | `https://api.sunrise-sunset.org/json?lat=18.52&lng=73.86&date=today` |
| **Dog CEO** | A random dog photo address | `https://dog.ceo/api/breeds/image/random` |
| **httpbin** | Shows you your own request: your headers and your address | `https://httpbin.org/get` |
| **Agify** | A guessed age for a first name | `https://api.agify.io/?name=priya&country_id=IN` |

## Change a request

Most of these APIs take values in the address after `?`. Change one value and call again:

- Open-Meteo: change `latitude` and `longitude`. Mumbai is `19.08` and `72.88`; Chennai is `13.08` and `80.27`.
- World Bank: change `IND` to another country's 3-letter code, such as `BGD`, `LKA` or `NPL`.
- India Post: change `411001` to your own PIN code.
- Frankfurter: change `USD` to `EUR` or `GBP`.

A broken request shows you how an API reports errors. For example, Open-Meteo answers `latitude=180` with status 400 and a JSON `reason`.

## Fair use

- **Be gentle:** these services are free. Do not call them in a fast loop. Agify allows 10 names a day without a key, and GitHub allows 60 requests an hour.
  Many APIs report your limit in the response headers: run `curl -si` and look for `x-rate-limit-limit` or `x-ratelimit-limit`.
- **Open-Meteo** is free for non-commercial use, and its data is under the CC BY 4.0 licence: say that the weather data comes from Open-Meteo.
- **Sunrise Sunset** asks you to show a link to sunrise-sunset.org when you use its data in an app.
- **Wikipedia** text is under the CC BY-SA licence. Name Wikipedia when you show it.
- **India Post PIN codes** (`api.postalpincode.in`) is a free community service, not an official India Post API. It can be slow; wait 30 seconds before you try again.

## Why REST Countries is not here

Older course material used REST Countries (`restcountries.com`). It has moved to version 5, which needs a free account and an API key. It has also switched off the old addresses (checked 10 November 2026).
Use the World Bank address above for country data.
