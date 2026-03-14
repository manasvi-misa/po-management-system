const express = require('express');
const http    = require('http');
const { Server } = require('socket.io');
const cors    = require('cors');

const app    = express();
const server = http.createServer(app);

// Allow frontend to connect
const io = new Server(server, {
  cors: { origin: '*', methods: ['GET', 'POST'] }
});

app.use(cors());
app.use(express.json());

// Store recent notifications in memory
const notifications = [];

// ── REST endpoint: Flask calls this when PO status changes ──
app.post('/notify', (req, res) => {
  const { reference_no, status, vendor } = req.body;

  const message = {
    id:           Date.now(),
    reference_no: reference_no || 'Unknown',
    status:       status       || 'Updated',
    vendor:       vendor       || '',
    time:         new Date().toLocaleTimeString()
  };

  // Save to memory
  notifications.unshift(message);
  if (notifications.length > 20) notifications.pop(); // keep last 20

  // Broadcast to ALL connected browsers instantly
  io.emit('po_status_changed', message);

  console.log(`[NOTIFY] ${message.reference_no} → ${message.status}`);
  res.json({ success: true, message });
});

// ── GET recent notifications ──
app.get('/notifications', (req, res) => {
  res.json(notifications);
});

// ── Socket connection log ──
io.on('connection', (socket) => {
  console.log(`[SOCKET] Client connected: ${socket.id}`);
  socket.on('disconnect', () => {
    console.log(`[SOCKET] Client disconnected: ${socket.id}`);
  });
});

// ── Start server ──
const PORT = 4000;
server.listen(PORT, () => {
  console.log(`Notification server running on http://localhost:${PORT}`);
});