const fetch = require('node-fetch');

describe('NWS /alerts endpoint', () => {
  const BASE_URL = 'https://api.weather.gov/alerts';

  test('should return alerts with status 200', async () => {
    const response = await fetch(`${BASE_URL}/active?area=NY`, {
      headers: { 'User-Agent': 'cs453-project (contact@example.com)' }
    });
    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data).toHaveProperty('features');
    expect(Array.isArray(data.features)).toBe(true);
  });

  test('should return alerts for the past 7 days', async () => {
    const response = await fetch(`${BASE_URL}?status=actual`, {
      headers: { 'User-Agent': 'cs453-project (contact@example.com)' }
    });
    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data).toHaveProperty('features');
  });

  test('should return 404 for invalid endpoint', async () => {
    const response = await fetch(`${BASE_URL}/invalid`, {
      headers: { 'User-Agent': 'cs453-project (contact@example.com)' }
    });
    expect(response.status).toBe(404);
  });
});