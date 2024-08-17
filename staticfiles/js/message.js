$(document).ready(function() {
    {% if messages %}
        var messageContent = "";
        {% for message in messages %}
            messageContent += "<div class='alert alert-{{ message.tags }}'>{{ message }}</div>";
        {% endfor %}
        $("#modalMessageContent").html(messageContent);
        $("#messageModal").modal('show');
    {% endif %}
});