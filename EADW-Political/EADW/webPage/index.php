<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <meta http-equiv="X-UA-Compatible" content="IE=edge, chrome=1"/>
        <title>EADW Political Searcher</title>
        <style>
			svg {
			  display: block;
			}
			#chart1 svg {
			  height: 500px;
			  min-width: 100px;
			  min-height: 100px;
			}
		</style>
		<link href="nvd3/src/nv.d3.css" rel="stylesheet" type="text/css">
		<script src="nvd3/lib/d3.v2.js"></script>
		<script src="nvd3/nv.d3.js"></script>
		<script src="nvd3/src/tooltip.js"></script>
		<script src="nvd3/src/utils.js"></script>
		<script src="nvd3/src/models/legend.js"></script>
		<script src="nvd3/src/models/axis.js"></script>
		<script src="nvd3/src/models/scatter.js"></script>
		<script src="nvd3/src/models/line.js"></script>
		<script src="nvd3/src/models/cumulativeLineChart.js"></script>
        <link href="css/reset.css" rel="stylesheet" type="text/css" />
        <link href="css/typo.css" rel="stylesheet" type="text/css" />
        <link href="css/layout.css" rel="stylesheet" type="text/css" />
        <script src="http://code.jquery.com/jquery-latest.min.js" type="text/javascript"></script>
        <link href='http://fonts.googleapis.com/css?family=Pontano+Sans' rel='stylesheet' type='text/css'>
        <link id="color" href="" rel="stylesheet" type="text/css" />
    </head>
    
<script>

function createGraph(data){
	$("#chart1").show()

	var chart;
    chart = nv.models.lineChart()
             .x(function(d) { return d[0] })
             .y(function(d) { return parseInt(d[1]) })
             .color(d3.scale.category10().range())
             .clipVoronoi(false);

   chart.xAxis
      .tickFormat(function(d) {
          return d3.time.format('%x')(new Date(d))
        });
        
   chart.yAxis
      .tickFormat(d3.format('d'));



  d3.select('#chart1 svg')
      .datum(data.data)
      .call(chart);

  nv.utils.windowResize(chart.update);

  chart.dispatch.on('stateChange', function(e) { nv.log('New State:', JSON.stringify(e)); });

  return chart;
}




</script>
<script>
	function showTopWords(){
		$("#chart1").hide()
		$.getJSON('../topWords/', function(result) {
					$("#results").empty();
					$("#results").append("<h3>TOP Words</h3>");
					//iterarar cada resultado
					$.each(result, function() {
						  $("#results").append("<p><b>"+this[1]+"</b>  "+this[0]+"</p>");
						});
					//preencher o template
					return false;
				});
	}
	
	function showTopCountries(){
		$("#chart1").hide()
		$.getJSON('../topCountries/', function(result) {
					$("#results").empty();
					$("#results").append("<h3>TOP Countries</h3>");
					//iterarar cada resultado
					$.each(result, function() {
						  $("#results").append("<p><b>"+this[1]+"</b>  "+this[0]+"</p>");
						});

					//preencher o template
					return false;
				});
	}
	
	function showTopPartidos(type){
		$.getJSON('../partidos'+type+'/', function(result) {
					$("#results").empty();
					$("#results").append("<h3>TOP Political Parties "+type+"</h3>");
					//iterarar cada resultado
					console.log(result);
					createGraph(result);

					//preencher o template
					return false;
				});
	}

</script>
    <script>
    	function valuesParser(values){
    		out = []
	    	for(i=0; i < values.length;i++){
		    	out.push([parseInt(values[i][0]),parseInt(values[i][1])]);
	    	}
	    	return out;
    	}
    	
		function getInfoEntity(name){
			$("#searchBox").val("");
			$("#chart1").show();
			$.getJSON('../entity/'+name, function(result) {
					$("#results").empty();
					$("#results").append(entityTemplate(result));
					});
		}
		
		function entityTemplate(entity){
			string = "<div class='entityDetails'>";
			string += "<h3 class='name'>"+entity.entity+"</h3>";
			if(entity.governo != null){
				string += "<p>Governo: "+entity.governo+"</p>";
			}
			if(entity.partido != null){
				string += "<p>Partido: "+entity.partido+"</p>";
			}
			string += "<p>Reputation: "+entity.reputation+"</p>";
			string += "<p>Adjectives: "+entity.adjectives	+"</p>";
			string += "</div>";
			createGraph(entity);
			return string;
		}
		
		function template(linke,title,summary,entities){
			string = '<div class="result_entry">';
			
			string += '<a href="'+linke+'"><h4 class="title">'+title+'</h4></a>';
		   string += '<p class="summary">'+summary+'</p>';
		   console.log(entities);
		   string += '<p class="entities">';
		   for(i = 0; i < entities.length; i++){
			   name = entities[i][0];
			   score = entities[i][1];
			   string += "<a onclick='getInfoEntity(\""+name+"\");'>"+name+" : "+score+"</a>";
		   }
		   string += '</p>';
		   string += "</div>";
		return string;
		}
	    	function myFunction()
			{
				var textToSearch = $("#searchBox").val();
				$.getJSON('../search/'+textToSearch, function(result) {
					$("#results").empty();
					//iterarar cada resultado
					if(result == []){
						setTimeout(function(){$("#results").append("<h1>Not found</h1>");}, 500);
						
					}
					$.each(result, function() {
						  console.log(this);
						  $("#results").append(template(this.link,this.title,this.summary,this.entities));
						});

					//preencher o template
					return false;
				});
				$("#chart1").hide()
				return false;
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
                   
                    <form action="" method="post" onsubmit="return myFunction();" id="searchForm" >
                    	<input style="width:400px" type="text" id="searchBox"></input>
                    </form>
                    <button type="button" onclick="myFunction()">Search</button>
                    <button type="button" onclick="showTopWords()">Top Words</button>
                    <button type="button" onclick="showTopCountries()">Top Countries</button>
                    <button type="button" onclick="showTopPartidos('Positive')">Political Parties Positive</button>
                    <button type="button" onclick="showTopPartidos('Neutral')">Political Parties Neutral</button>
                    <button type="button" onclick="showTopPartidos('Negative')">Political Parties Negative</button>
                    <button type="button" onclick="showTopPartidos('Opinion')">Political Parties Opinion</button>

                    <div id="results">
                    	
                    </div>
                      <div id="chart1">
    <svg style="height: 400px;width:800px"></svg>
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
