$(document).ready(function(){

  var one_hundred_column = $('#row-100-liters, #row-100-rate, #row-100-index');
  var three_hundred_column = $('#row-300-liters, #row-300-rate, #row-300-index');
  var five_hundred_column = $('#row-500-liters, #row-500-rate, #row-500-index');
  var nine_hundred_column = $('#row-900-liters, #row-900-rate, #row-900-index');
  
  var my_columns = (one_hundred_column, three_hundred_column, five_hundred_column, nine_hundred_column); 


  $('#check_100').change(function()
  {
      if (this.checked) 
      {
        $(one_hundred_column).show();
      } 
      else 
      {
        $(one_hundred_column).hide();
      } 
               
  });

  $('#check_300').change(function()
  {
      if (this.checked) 
      {
        $(three_hundred_column).show();
      } 

      else 
      {
        $(three_hundred_column).hide();
      } 
  });

  $('#check_500').change(function()
  {
      if (this.checked) 
      {
        $(five_hundred_column).show();
      } 

      else 
      {
        $(five_hundred_column).hide();
      } 
  });

  $('#check_900').change(function()
  {
      if (this.checked) 
      {
        $(nine_hundred_column).show();
      } 

      else 
      {
        $(nine_hundred_column).hide();
      } 
  });

});



