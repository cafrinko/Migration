$('.animal_id').on('click', function(evt) {
    evt.preventDefault();
    var url = $(this).data('target');
    location.replace(url);
})