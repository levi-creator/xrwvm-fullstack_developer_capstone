const mongoose = require('mongoose');

const reviewSchema = new mongoose.Schema({
  id: { type: Number, required: true },
  dealership: { type: Number, required: true }, // ✅ matches your JSON payload
  name: { type: String, required: true },
  review: { type: String, required: true },
  purchase: { type: Boolean, required: true },
  purchase_date: { type: String },
  car_make: { type: String },
  car_model: { type: String },
  car_year: { type: Number }
});

module.exports = mongoose.model('Review', reviewSchema);
