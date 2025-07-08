const axios = require('axios');

async function testForecast() {
  try {
    const payload = {
      "Type of Soil": "Sample Soil",
      "Type/Variety": "Sample Variety",
      "Location": "Sample Location",
      "Type of Crops": "Sample Crop",
      "Week 1": 10,
      "Week 2": 12,
      "Week 3": 11,
      "Week 4": 13,
      "Month": "January",
      "Year": 2024
    };

    const response = await axios.post('http://127.0.0.1:5000/forecast', payload, {
      headers: {
        'Content-Type': 'application/json'
      }
    });

    console.log('Forecast response:', response.data);
  } catch (error) {
    if (error.response) {
      console.error('Error response:', error.response.data);
    } else {
      console.error('Error:', error.message);
    }
  }
}

testForecast(); 