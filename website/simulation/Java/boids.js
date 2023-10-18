const canvas = document.getElementById("bgCanvas");
const ctx = canvas.getContext("2d");

// Define a new Path:
ctx.beginPath();

// Define a start Point
ctx.moveTo(0, 0);

// Define an end Point
ctx.lineTo(200, 100);

// Stroke it (Do the Drawing)
ctx.stroke();