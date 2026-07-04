// MemeTide WebSocket Demo - Copy & Paste into Browser Console
// For demo video recording

console.clear();
console.log('🌊 MemeTide WebSocket Demo');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

const ws = new WebSocket('wss://memetide-production.up.railway.app/ws/alerts?client_id=demo_video');

ws.onopen = () => {
  console.log('✅ WebSocket Connected');
  console.log('📡 Subscribing to PEPE and FLOKI...');
  
  ws.send(JSON.stringify({
    command: 'subscribe',
    tokens: ['PEPE', 'FLOKI']
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.type === 'connection') {
    console.log('🔗 Connection confirmed:', data.message);
  }
  
  if (data.type === 'subscribed') {
    console.log('✅ Subscribed to:', data.tokens.join(', '));
    console.log('🔔 Now listening for real-time alerts...');
  }
  
  if (data.type === 'token_alert') {
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('🔥 NEW ALERT:', data.token.symbol);
    console.log('   Score:', data.token.score);
    console.log('   Confidence:', data.token.confidence);
    console.log('   Risk:', data.token.risk_level);
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  }
  
  if (data.type === 'scan_complete') {
    console.log('📊 Scan complete:', data.message);
    console.log('   Tokens found:', data.tokens_count);
  }
};

ws.onerror = (error) => {
  console.error('❌ WebSocket Error:', error);
};

ws.onclose = () => {
  console.log('🔌 WebSocket Disconnected');
};

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('Waiting for alerts... (this may take a few seconds)');
