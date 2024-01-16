function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Obter o token CSRF e definir csrftoken
var csrftoken = getCookie('csrftoken');

$(document).ready(function() {
    $(document).on('click', '.select-btn', function() {
        selectChar($(this).data('char-id'));
    });
});



$(document).ready(function() {
    function updateCharList() {
        $('#char-list').empty();

        $.ajax({
            url: '/Game/get_all_chars/',
            method: 'GET',
            success: function(data) {
                data.forEach(function(char) {
                    $('#char-list').append('<li>' + char.name + ' - ' + char.job +
                        '<button class="delete-btn" data-char-id="' + char.name + '">Delete Char</button>' +
                        '<button class="select-btn" data-char-name="' + char.name + '">Select Char</button></li>');
                });
            },
            error: function() {
                console.error('Error fetching characters.');
            }
        });
    }

    updateCharList();
});



$(document).ready(function() {
    $(document).on('click', '.select-btn', function() {
        selectChar($(this).data('char-name'));
    });
});

function selectChar(charName) {
    $.ajax({
        url: '/Game/select_char/',
        method: 'POST',
        data: { 'name': charName },
        headers: { 'X-CSRFToken': csrftoken },
        success: function(response) {
            // Redirecione para a página do jogo com as informações do personagem como parâmetros na URL
            window.location.href = '/Game/Game.html?' + $.param(response);
        }
    });
}

$(document).ready(function() {
    $(document).on('click', '.delete-btn', function() {
        deleteChar($(this).data('char-id'));
    });
});

function deleteChar(charName) {
    var csrftoken = getCookie('csrftoken');

    $.ajax({
        url: '/Game/delete_char/',
        method: 'POST',
        data: { 'name': charName },
        headers: { 'X-CSRFToken': csrftoken },
        success: function(response) {
           console.log('Select success:', response.message);
            // Se necessário, adicione um redirecionamento aqui
        },
        error: function(xhr, status, error) {
            console.error('Error selecting char:', status, error);
        }
    });
}
