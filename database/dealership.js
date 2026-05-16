const mongoose = require('mongoose');

const dealershipSchema = new mongoose.Schema({
  id: { type: Number, required: true },
  city: { type: String, required: true },
  state: { type: String, required: true },
  st: { type: String },
  address: { type: String },
  zip: { type: String },
  lat: { type: Number },
  long: { type: Number }
});

module.exports = mongoose.model('Dealership', dealershipSchema);
