// static/scripts.js
document.getElementById('taskForm').addEventListener('submit', function(e) {
    e.preventDefault();
    fetch('/add', {
        method: 'POST',
        body: new FormData(this)
    }).then(response => response.json())
      .then(data => {
          if (data.result) console.log(data.result);
      });
});

var socket = io();

socket.on('connect', function() {
    console.log('Connected to server');
});

socket.on('task_added', function(data) {
    var list = document.getElementById('tasks');
    var newTask = document.createElement('li');
    newTask.innerHTML = `<span>${data.title}</span><button onclick="updateTask(${data.id})">Update</button><button onclick="deleteTask(${data.id})">Delete</button><input type="checkbox" onchange="updateTask(${data.id})">`;
    list.appendChild(newTask);
});

function updateTask(id) {
    // Implement update logic, possibly with a form or modal
}

function deleteTask(id) {
    fetch(`/delete/${id}`, { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        if (data.result) {
            document.querySelector(`li button[onclick="deleteTask(${id})"]`).parentNode.remove();
        }
    });
}

socket.on('task_updated', function(data) {
    // Handle task update in the UI
});

socket.on('task_deleted', function(data) {
    // Remove the task from the UI
    document.querySelector(`li button[onclick="deleteTask(${data.id})"]`).parentNode.remove();
});