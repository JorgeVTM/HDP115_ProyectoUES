

$('#btn-sidebar').click(function() {    
    $('#sidebar').animate({
        width: '0',
    }, 'slow');
});

$('#logo').click(function() {
    $('#sidebar').animate({
        width: '250px',
    }, 'slow');
});
