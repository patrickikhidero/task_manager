// static/script.js

$(document).ready(function() {
    const socket = io.connect('http://localhost:5000'); // Change to your actual URL

    function fetchTasks() {
        $.get('/tasks', function(tasks) {
            $('#task-list').empty();
            tasks.forEach(task => {
                $('#task-list').append(`
                    <li class="list-group-item" id="task-${task.id}">
                        <strong>${task.title}</strong><br>
                        ${task.description}<br>
                        <input type="checkbox" ${task.completed ? 'checked' : ''} onchange="updateTask(${task.id}, this.checked)"> Completed
                        <button class="btn btn-danger btn-sm float-right" onclick="deleteTask(${task.id})">Delete</button>
                    </li>
                `);
            });
        });
    }

    $('#task-form').submit(function(e) {
        e.preventDefault();
        const title = $('#task-title').val();
        const description = $('#task-description').val();

        $.ajax({
            type: 'POST',
            url: '/tasks',
            contentType: 'application/json',
            data: JSON.stringify({ title, description }),
            success: function() {
                $('#task-title').val('');
                $('#task-description').val('');
                fetchTasks();
            }
        });
    });

    socket.on('task_updated', function(data) {
        fetchTasks();
    });

    window.updateTask = function(taskId, completed) {
        $.ajax({
            type: 'PUT',
            url: `/tasks/${taskId}`,
            contentType: 'application/json',
            data: JSON.stringify({ completed }),
            success: function() {
                console.log('Task updated');
            }
        });
    };

    window.deleteTask = function(taskId) {
        $.ajax({
            type: 'DELETE',
            url: `/tasks/${taskId}`,
            success: function() {
                console.log('Task deleted');
                fetchTasks();
            }
        });
    };

    // Fetch initial tasks
    fetchTasks();
});

