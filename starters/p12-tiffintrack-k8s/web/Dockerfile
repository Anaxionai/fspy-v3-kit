# The TiffinTrack web image (task 9): nginx serves the built page at /. Build it from tiffintrack/:
#   docker build -t tiffintrack-web:0.1.0 web

# Build stage: install the locked packages and build the page into dist/.
FROM node:24-alpine AS build
WORKDIR /web
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# Final stage: nginx with the built files only.
FROM nginx:1.30-alpine
COPY --from=build /web/dist /usr/share/nginx/html
EXPOSE 80
