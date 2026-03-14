const express = require('express');
const http    = require('http');
const { Server } = require('socket.io');
const cors    = require('cors');

const app    = express();
const server = http.createServer(app);

const io = new Server(server, {
  cors: { origin: '*', methods: ['GET', 'POST'] }
});

app.use(cors());
app.use(express.json());

const notifications = [];

app.post('/notify', (req, res) => {
  const { reference_no, status, vendor } = req.body;

  const message = {
    id:           Date.now(),
    reference_no: reference_no || 'Unknown',
    status:       status       || 'Updated',
    vendor:       vendor       || '',
    time:         new Date().toLocaleTimeString()
  };

  notifications.unshift(message);
  if (notifications.length > 20) notifications.pop(); 

  io.emit('po_status_changed', message);

  console.log(`[NOTIFY] ${message.reference_no} → ${message.status}`);
  res.json({ success: true, message });
});

app.get('/notifications', (req, res) => {
  res.json(notifications);
});

io.on('connection', (socket) => {
  console.log(`[SOCKET] Client connected: ${socket.id}`);
  socket.on('disconnect', () => {
    console.log(`[SOCKET] Client disconnected: ${socket.id}`);
  });
});

const PORT = 4000;
server.listen(PORT, () => {
  console.log(`Notification server running on http://localhost:${PORT}`);
});