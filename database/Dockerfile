FROM node:18.12.1-bullseye-slim

RUN npm install -g npm@9.1.3

WORKDIR /usr/src/app

# Copy project files
COPY package.json .
COPY app.js .
COPY review.js .
COPY dealership.js .
RUN mkdir -p data
COPY data/dealerships.json ./data/dealerships.json
COPY data/reviews.json ./data/reviews.json
COPY . .

RUN npm install

EXPOSE 3030

CMD ["node", "app.js"]
