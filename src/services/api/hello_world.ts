const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || '';

export const helloWorldApi = {
  // Get hello world message
  getHelloWorld: async () => {
    const response = await fetch(`${API_BASE_URL}/api/hello_world/get_hello_world`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    return response.json();
  },

  // Post hello world message with name
  postHelloWorld: async (name: string) => {
    const response = await fetch(`${API_BASE_URL}/api/hello_world/post_hello_world`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name })
    });
    return response.json();
  }
};
