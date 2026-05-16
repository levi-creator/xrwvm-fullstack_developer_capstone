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
app.use(express.json());
app.use(bodyParser.json());

// Load seed data from data/ folder
const reviews_data = JSON.parse(fs.readFileSync('./data/reviews.json', 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync('./data/dealerships.json', 'utf8'));

mongoose.connect('mongodb://mongo_db:27017/', { dbName: 'dealershipsDB' });

(async () => {
  try {
    await Review.deleteMany({});
    await Review.insertMany(reviews_data.reviews);
    await Dealership.deleteMany({});
    await Dealership.insertMany(dealerships_data.dealerships);
    console.log('✅ Database seeded successfully');
  } catch (error) {
    console.error('Error seeding data:', error);
  }
})();

app.get('/', (req, res) => res.send('Welcome to the Mongoose API'));

app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Review.find();
    res.json(documents);
  } catch {
    res.status(500).json({ error: 'Error fetching reviews' });
  }
});

app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const documents = await Review.find({ dealership: parseInt(req.params.id) });
    res.json(documents);
  } catch {
    res.status(500).json({ error: 'Error fetching reviews by dealer' });
  }
});

app.get('/fetchDealers', async (req, res) => {
  try {
    const documents = await Dealership.find();
    res.json(documents);
  } catch {
    res.status(500).json({ error: 'Error fetching dealerships' });
  }
});

app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const documents = await Dealership.find({ state: req.params.state });
    res.json(documents);
  } catch {
    res.status(500).json({ error: 'Error fetching dealerships by state' });
  }
});

app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const document = await Dealership.findOne({ id: parseInt(req.params.id) });
    res.json(document);
  } catch {
    res.status(500).json({ error: 'Error fetching dealer by id' });
  }
});

app.post('/postReview', async (req, res) => {
  try {
    console.log('Incoming review payload:', req.body);
    const documents = await Review.find().sort({ id: -1 });
    const new_id = documents.length > 0 ? documents[0].id + 1 : 1;

    const review = new Review({ id: new_id, ...req.body });
    await review.save();

    res.json({ status: 'success', id: new_id });
  } catch (error) {
    console.error('Error inserting review:', error.message);
    res.status(500).json({ error: error.message });
  }
});

app.listen(port, () => {
  console.log(`🚀 Server is running on http://localhost:${port}`);
});
