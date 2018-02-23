var submitAnswer = function(problem_id) {
    
      var radios = $('input',problem_id)
      var val= "";
      for (var i = 0, length = radios.length; i < length; i++) {
          if (radios[i].checked) {
             val = radios[i].value; 
             break;
           }
      }
      $('p.answer',problem_id).empty()
      if (val == "" ) {        
        $('p.answer',problem_id).text('Seleccione una respuesta')
        $('p.answer',problem_id).removeClass( "incorrecta correcta" ).addClass( "nada" );
      } else if ( val == "true" ) {        
        $('p.answer',problem_id).text('Respuesta Correcta');
        $('p.answer',problem_id).append($('<span class="glyphicon glyphicon-ok" aria-hidden="true"></span>'));    
        $('p.answer',problem_id).removeClass( "incorrecta nada" ).addClass( "correcta" );
      } else {
        $('p.answer',problem_id).text('Respuesta Incorrecta')
        $('p.answer',problem_id).append($('<span class="glyphicon glyphicon-remove" aria-hidden="true"></span>'));    
        $('p.answer',problem_id).removeClass( "correcta nada" ).addClass( "incorrecta" );
      }
    };