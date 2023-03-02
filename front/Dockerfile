FROM node:16.16-alpine as builder

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
ENV PATH /usr/src/app/node_modules/.bin:$PATH
COPY package.json /usr/src/app/
RUN yarn install --silent
COPY . /usr/src/app
RUN NODE_ENV=production URL_API=http://127.0.0.1:8004 yarn build
#RUN NODE_ENV=production npm run generate

FROM node:16.16-alpine
COPY --from=builder /usr/src/app /usr/src/app
WORKDIR /usr/src/app
ENV HOST=0.0.0.0 PORT=80
EXPOSE 80
CMD [ "yarn", "start" ]

#FROM nginx:stable-alpine
#COPY --from=builder /usr/src/app/dist /usr/share/nginx/html
#EXPOSE 80
#CMD ["nginx", "-g", "daemon off;"]
