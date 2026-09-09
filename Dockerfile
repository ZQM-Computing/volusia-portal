# syntax=docker/dockerfile:1
# Project Volusia — Public Data Portal
# Multi-stage build: compile React app, serve via nginx

FROM node:20-alpine AS build
WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install --silent

COPY . .
RUN npm run build

FROM nginx:alpine AS serve
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
COPY --from=build /app/public /usr/share/nginx/html/public
COPY --from=build /app/data /usr/share/nginx/html/data

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
