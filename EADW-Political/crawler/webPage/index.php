<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <meta http-equiv="X-UA-Compatible" content="IE=edge, chrome=1"/>
        <title>EADW Political Searcher</title>
        <link href="css/reset.css" rel="stylesheet" type="text/css" />
        <link href="css/typo.css" rel="stylesheet" type="text/css" />
        <link href="css/layout.css" rel="stylesheet" type="text/css" />
        <script src="http://code.jquery.com/jquery-latest.min.js" type="text/javascript"></script>
        <link href="css/validationEngine.jquery.css" rel="stylesheet" type="text/css" />
        <link href='http://fonts.googleapis.com/css?family=Pontano+Sans' rel='stylesheet' type='text/css'>
        <link id="color" href="" rel="stylesheet" type="text/css" />
    </head>
    <script>
		function template(title,summary,entities){
			string = '';
			string += '<a href="http://www.ist.utl.pt/"><h4 class="title">'+title+'</h4></a>';
		   string += '<p class="summary">'+summary+'</p>';
		   string += '<p class="entities">'+entities+'</p>';
		return string;
		}
	    	function myFunction()
			{
				var textToSearch = $("#searchBox").val();
				$.getJSON('../search/2', function(result) {
					$("#results").empty();
					//iterarar cada resultado
					$.each(result, function() {
						  console.log(this);
						  $("#results").append(template(this.title,this.summary,this.entities));

						});



					//preencher o template
					
				});
			}
    </script>
    <body>
        <!-- Root container for all elements -->
        <div id="rootContainer">
            <div id="rootContainerLayer">
                
                <img id="ie8Corner" src="images/ie8-bg.png" />
                
                <!-- Home page -->
                <div id="homePage">

                    <!-- Your name and position -->
                    <h1>EADW Political Searcher</h1>
                    <h2>Artur Balanuta, Dário Nascimento</h2>
                   
                    <form id="searchForm" >
                    	<input style="width:400px" type="text" id="searchBox"></input>
                    </form>
                    <button type="button" onclick="myFunction()">Search</button>
                    <div id="results">
                    	
                    </div>
                </div>
            </div>
        </div>
        <!-- Copyright -->
        <p id="copyright">
            <span>2013 &copy; Instituto Superior Técnico</span>
        </p>
    </body>
</html>
