

$('#btn-sidebar').click(function() {    
    $('.ventana-bloqueo').animate({opacity: '0',}, 'slow');
    $('#sidebar').animate({width: '0',}, 'slow', function(){
        $('.ventana-bloqueo').css('display', 'none');
    });
    $('body').css('overflow', 'initial');
});

$('.ventana-bloqueo').click(function() {    
    $('.ventana-bloqueo').animate({opacity: '0',}, 'slow');
    $('#sidebar').animate({width: '0',}, 'slow', function(){
        $('.ventana-bloqueo').css('display', 'none');
    });
    $('body').css('overflow', 'initial');
});

$('#logo').click(function() {
    $('body').css('overflow', 'hidden');
    $('.ventana-bloqueo').css('display', 'initial');
    $('#sidebar').animate({width: '250px',}, 'slow');
    $('.ventana-bloqueo').animate({opacity: '.75',}, 'slow');
});
