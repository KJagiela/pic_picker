ARG NODE_VERSION=16.14-buster

FROM node:${NODE_VERSION} as develop-stage

ARG BUILD_ENVIRONMENT=local

WORKDIR /app

RUN npm install yarn

RUN yarn global add @quasar/cli http-server

COPY frontend/package.json frontend/yarn.lock /app/

RUN yarn install

CMD ["quasar", "dev", "-H", "0.0.0.0"]

FROM develop-stage as build-stage

COPY . ./

RUN yarn install

RUN quasar build
WORKDIR /app/dist/spa
CMD ["quasar", "serve", "-H", "0.0.0.0", "-p", "8080"]

FROM nginx:1.21 as production-stage

COPY --from=build-stage /app/dist/spa /usr/share/nginx/html

COPY ./compose/default.conf /default.conf
COPY ./compose/start.sh /start.sh

RUN chmod +x /start.sh

CMD ["/start.sh"]
