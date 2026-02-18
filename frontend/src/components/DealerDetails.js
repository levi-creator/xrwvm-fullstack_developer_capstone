import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function DealerDetails() {
  const { id } = useParams();
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch(`/django/dealer_details/${id}`)
      .then(res => res.json())
      .then(data => setData(data))
      .catch(err => console.error("Error fetching dealer details:", err));
  }, [id]);

  if (!data) return <p>Loading...</p>;

  return (
    <div>
      <h2>{data?.dealer?.full_name}</h2>
      <p>{data?.dealer?.city}, {data?.dealer?.state}</p>

      <h3>Cars Available</h3>
      <ul>
        {data.cars.map((car, idx) => (
          <li key={idx}>
            {car.year} {car.make} {car.model} ({car.type})
          </li>
        ))}
      </ul>

      <h3>Customer Reviews</h3>
      <ul>
        {data.reviews.map((review, idx) => (
          <li key={idx}>
            <strong>{review.name}:</strong> {review.review}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default DealerDetails;
