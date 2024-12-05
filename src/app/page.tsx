'use client';
import { useState } from 'react';
import { helloWorldApi } from '@/services/api/hello_world';

export default function Home() {
  const [getMessage, setGetMessage] = useState<string>('');
  const [name, setName] = useState<string>('');
  const [postMessage, setPostMessage] = useState<string>('');

  const handleGetHelloWorld = async () => {
    try {
      const response = await helloWorldApi.getHelloWorld();
      setGetMessage(response.message || 'No message received');
    } catch (error) {
      setGetMessage('Error fetching message');
    }
  };

  const handlePostHelloWorld = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name) return;
    
    try {
      const response = await helloWorldApi.postHelloWorld(name);
      setPostMessage(response.message || 'No message received');
    } catch (error) {
      setPostMessage('Error sending message');
    }
  };

  return (
    <main className="p-8">
      <div className="max-w-md mx-auto space-y-8">
        {/* GET Request Section */}
        <div className="space-y-4">
          <h2 className="text-xl font-bold">Test GET Request</h2>
          <button
            onClick={handleGetHelloWorld}
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            Get Hello World
          </button>
          {getMessage && (
            <p className="mt-2">{getMessage}</p>
          )}
        </div>

        {/* POST Request Section */}
        <div className="space-y-4">
          <h2 className="text-xl font-bold">Test POST Request</h2>
          <form onSubmit={handlePostHelloWorld} className="space-y-4">
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Enter your name"
              required
              className="w-full px-4 py-2 border rounded"
            />
            <button
              type="submit"
              className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
            >
              Send Hello World
            </button>
          </form>
          {postMessage && (
            <p className="mt-2">{postMessage}</p>
          )}
        </div>
      </div>
    </main>
  );
}
