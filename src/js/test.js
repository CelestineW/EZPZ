 $(document).ready(function () {
     $('<div/>', {
         'class' : 'extraPerson', html: GetHtml()
     }).appendTo('#container');
     $('#addRow').click(function () {
           $('<div/>', {
               'class' : 'extraPerson', html: GetHtml()
     }).hide().appendTo('#container').slideDown('slow');
         
     });
 })
 function GetHtml()
{
      var len = $('.extraPerson').length;
    var $html = $('.extraPersonTemplate').clone();
    $html.find('[name=firstname]')[0].name="firstname" + len;
    $html.find('[name=lastname]')[0].name="lastname" + len;
    $html.find('[name=gender]')[0].name="gender" + len;
    return $html.html();    
}