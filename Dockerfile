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
COPY --from=build /app/public/favicon.svg /usr/share/nginx/html/favicon.svg

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
