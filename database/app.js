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
app.use(bodyParser.json()); // ✅ use JSON parser for POST requests

// Load seed data
const reviews_data = JSON.parse(fs.readFileSync("reviews.json", 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync("dealerships.json", 'utf8'));

// Connect to MongoDB
mongoose.connect("mongodb://mongo_db:27017/", { dbName: 'dealershipsDB' });

// Seed collections
(async () => {
  try {
    await Review.deleteMany({});
    await Review.insertMany(reviews_data['reviews']);
    await Dealership.deleteMany({});
    await Dealership.insertMany(dealerships_data['dealerships']);
    console.log("✅ Database seeded successfully");
  } catch (error) {
    console.error("Error seeding data:", error);
  }
})();

// Routes
app.get('/', (req, res) => res.send("Welcome to the Mongoose API"));

// Fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Review.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching reviews' });
  }
});

// Fetch reviews for a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const documents = await Review.find({ dealership: parseInt(req.params.id) });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching reviews by dealer' });
  }
});

// Fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
  try {
    const documents = await Dealership.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealerships' });
  }
});

// Fetch dealerships by state
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const documents = await Dealership.find({ state: req.params.state });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealerships by state' });
  }
});

// Fetch dealer by id
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const document = await Dealership.findOne({ id: parseInt(req.params.id) });
    res.json(document);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealer by id' });
  }
});

// Insert a new review
app.post('/insert_review', async (req, res) => {
  try {
    // Find highest existing id
    const documents = await Review.find().sort({ id: -1 });
    let new_id = documents.length > 0 ? documents[0].id + 1 : 1;

    // Create and save new review
    const review = new Review({ id: new_id, ...req.body });
    await review.save();

    res.json({ status: "success", id: new_id });
  } catch (error) {
    console.error("Error inserting review:", error);
    res.status(500).json({ error: "Error inserting review" });
  }
});

// Start server
app.listen(port, () => {
  console.log(`🚀 Server is running on http://localhost:${port}`);
});
