    /********************************************************
     * This is the actual example part where we call grabStrength
     *****************************************************/

    var output = document.getElementById('output'),
        progress = document.getElementById('progress'),
        handshape = document.getElementById('handshape');

    $('#rock').hide();
    $('#paper').hide();
    $('#scissors').hide();

    var myFirebaseRef = new Firebase("https://rpsuh16.firebaseio.com/games");
    myFirebaseRef.child(firebaseID).child("value").on("value", function(snapshot) {
      console.log(snapshot.val());
      // document.getElementById('ai').innerHTML = "AI thinks you played";

      $('#rock').hide();
      $('#paper').hide();
      $('#scissors').hide();
       $("#ai-guess").show();
      if (snapshot.val() == 'P') {
            // document.getElementById('ai').innerHTML += "Paper\nAI PLAYS <strong>SCISSORS!!!</strong>";
            $('#scissors').show();
      }
      else if (snapshot.val() == 'R') {
            // document.getElementById('ai').innerHTML += "Rock\nAI PLAYS <strong>PAPER!!!</strong>";
            $('#paper').show();
      }
      else if (snapshot.val() == 'S') {
            // document.getElementById('ai').innerHTML += "Scissors\nAI PLAYS <strong>ROCK!!!</strong>";
            $('#rock').show();
      }
      else if (snapshot.val() == 'ARGH') {
            document.getElementById('ai').innerHTML += "IDK";
      }
      else {
            document.getElementById('ai').innerHTML = "";
      }
    }, function (errorObject) {
      console.log("The read failed: " + errorObject.code);
    });

    myFirebaseRef.child(firebaseID).child("training").on("value", function(snapshot) {
      console.log(snapshot.val());
      if (snapshot.val() == 'P') {
            document.body.style.backgroundColor = "yellow";
            document.getElementById('ai').innerHTML = "Training : Paper";
      }
      else if (snapshot.val() == 'R') {
            document.body.style.backgroundColor = "yellow";
            document.getElementById('ai').innerHTML = "Training : Rock";
      }
      else if (snapshot.val() == 'S') {
            document.body.style.backgroundColor = "yellow";
            document.getElementById('ai').innerHTML = "Training : Scissors";
      }
      else {
            document.body.style.backgroundColor = "transparent";
            document.getElementById('ai').innerHTML = "";
      }
    }, function (errorObject) {
      console.log("The read failed: " + errorObject.code);
    });

    myFirebaseRef.child(firebaseID).child("confidence").on("value", function(snapshot) {
      console.log(snapshot.val());
      if (snapshot.val() == '1') {
            $("#ai-guess").show();
      }
      else {
            $("#ai-guess").hide();
      }
    }, function (errorObject) {
      console.log("The read failed: " + errorObject.code);
    });


    // Set up the controller:
    Leap.loop({background: true}, {

        hand: function(hand){
            var f = 0;
            for(var i=0;i<hand.fingers.length;i++){
                if(hand.fingers[i].extended){
                    f++;
                }
            }
            if( f == 2 ) {
                    handshape.innerHTML = "S";
            }
            else if( f > 2 ) {
                handshape.innerHTML = "P";     
            }
            else {
                handshape.innerHTML = "R";
            }
        }

    });


    /*********************************************************
     * End of the actual example
     ****************************************************/


    /*********************************************************
     * The rest of the code is here for visualizing the example. Feel
     * free to remove it to experiment with the API value only
     ****************************************************/

    // Adds the rigged hand and playback plugins
    // to a given controller, providing a cool demo.
    visualizeHand = function(controller){
        // The leap-plugin file included above gives us a number of plugins out of the box
        // To use a plugins, we call `.use` on the controller with options for the plugin.
        // See js.leapmotion.com/plugins for more info

        controller.use('riggedHand', {
            scale: 0.01,
            boneColors: function (boneMesh, leapHand){
                if ((boneMesh.name.indexOf('Finger_') == 0) ) {
                    return {
                        hue: 0.564,
                        saturation: leapHand.grabStrength
            
                    }
                }
            },
            checkWebGL: true
        }).on('riggedHand.meshAdded', function(handMesh, leapHand){
            handMesh.material.opacity = 1;
            handMesh.castShadow == true;
        });

        var camera = controller.plugins.riggedHand.camera;
        camera.position.set(0,500,0);
        camera.lookAt(new THREE.Vector3(0,0,0));
        camera.position.set(0,500,-100);
    };
    visualizeHand(Leap.loopController);    