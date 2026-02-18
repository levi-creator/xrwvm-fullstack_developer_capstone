const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const port = 3030;

const Review = require('./review');
const Dealership = require('./dealership');

app.use(cors());
app.use(bodyParser.urlencoded({ extended: false }));

const reviews_data = JSON.parse(fs.readFileSync("reviews.json", 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync("dealerships.json", 'utf8'));

mongoose.connect("mongodb://mongo_db:27017/", { dbName: 'dealershipsDB' });

try {
  Review.deleteMany({}).then(() => {
    Review.insertMany(reviews_data['reviews']);
  });
  Dealership.deleteMany({}).then(() => {
    Dealership.insertMany(dealerships_data['dealerships']);
  });
} catch (error) {
  console.error("Error seeding data:", error);
}

// Routes
app.get('/', (req, res) => res.send("Welcome to the Mongoose API"));

app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Review.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching reviews' });
  }
});

app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const documents = await Review.find({ dealership: req.params.id });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching reviews by dealer' });
  }
});

app.get('/fetchDealers', async (req, res) => {
  try {
    const documents = await Dealership.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealerships' });
  }
});

app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const documents = await Dealership.find({ state: req.params.state });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealerships by state' });
  }
});

app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const document = await Dealership.findOne({ id: parseInt(req.params.id) });
    res.json(document);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealer by id' });
  }
});

app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
  const data = JSON.parse(req.body);
  const documents = await Review.find().sort({ id: -1 });
  let new_id = documents[0]['id'] + 1;

  const review = new Review({ id: new_id, ...data });

  try {
    Review.deleteMany({}).then(() => {
      Review.insertMany(reviews_data['reviews']);
    });
    Dealership.deleteMany({}).then(() => {
      Dealership.insertMany(dealerships_data['dealerships']);
    });
  } catch (error) {
    console.error("Error seeding data:", error);
  }
  
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
