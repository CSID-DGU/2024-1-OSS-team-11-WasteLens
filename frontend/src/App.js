import React, { useState } from 'react';
import axios from 'axios';

const ImageUpload = () => {
  const [image, setImage] = useState(null);
  const [detectionResults, setDetectionResults] = useState([]);

  const handleImageChange = (e) => {
    setImage(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('image', image);

    try {
      const response = await axios.post('http://localhost:8000/api/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.success) {
        const imageId = response.data.image_id;
        const detectionResponse = await axios.get(`http://localhost:8000/api/detection-results/${imageId}/`);
        setDetectionResults(detectionResponse.data);
      }
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleImageChange} />
        <button type="submit">Upload</button>
      </form>
      <ul>
        {detectionResults.map((result, index) => (
          <li key={index}>
            Label: {result.label}, Confidence: {result.confidence.toFixed(2)}, Box: ({result.x_min}, {result.y_min}) ({result.x_max}, {result.y_max})
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ImageUpload;