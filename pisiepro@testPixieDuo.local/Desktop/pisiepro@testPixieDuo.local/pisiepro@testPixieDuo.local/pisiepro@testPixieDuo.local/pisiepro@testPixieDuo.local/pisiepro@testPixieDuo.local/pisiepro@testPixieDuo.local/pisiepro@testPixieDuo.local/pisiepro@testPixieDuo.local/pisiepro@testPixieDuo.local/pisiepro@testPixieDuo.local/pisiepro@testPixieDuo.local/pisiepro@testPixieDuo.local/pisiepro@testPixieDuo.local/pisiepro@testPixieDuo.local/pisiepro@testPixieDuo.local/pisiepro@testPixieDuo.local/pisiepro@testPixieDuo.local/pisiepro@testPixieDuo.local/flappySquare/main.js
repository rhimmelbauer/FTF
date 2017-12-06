var score;
var go = 0;
var startRequested;
var stopRequested;

var mainState = {
    
    preload: function() { 
    
    game.load.image('bird', 'assets/bird.png'); 
    game.load.image('pipe', 'assets/pipe.png');
    },

    create: function() { 
        
        if (game.device.desktop == false) {
        
            game.scale.scaleMode = Phaser.ScaleManager.SHOW_ALL;

            game.scale.setMinMax(game.width/2, game.height/2,
                                 game.width, game.height);

            game.scale.pageAlignHorizontally = true;
            game.scale.pageAlignVertically = true;
        }

        game.stage.backgroundColor = '#71c5cf';
        game.physics.startSystem(Phaser.Physics.ARCADE);
        this.bird = game.add.sprite(100, 245, 'bird');
        game.physics.arcade.enable(this.bird);
        this.bird.body.gravity.y = 1000;  

        var spaceKey = game.input.keyboard.addKey(
                        Phaser.Keyboard.SPACEBAR);
        spaceKey.onDown.add(this.jump, this);     

        this.pipes = game.add.group(); 
        this.timer = game.time.events.loop(1500, this.addRowOfPipes, this); 

        this.score = 0;
        this.labelScore = game.add.text(20, 20, "0", 
            { font: "30px Arial", fill: "#ffffff" });
        score = this.score;

        game.input.onDown.add(this.jump, this);

        go = game.add.text((game.width/2) , (game.height/2),"GO!",
                                 { font: "50px Arial", fill: "#ffff00" });
        go.anchor.setTo(0.5,0.5);

        game.paused = true;
        startRequested = false;
        stopRequested = false;
    },

    update: function() {

        if(game.paused){           
            return;
        }
        
        if (this.bird.y < 0 || this.bird.y > 490)
            this.restartGame();
        game.physics.arcade.overlap(
            this.bird, this.pipes, this.restartGame, null, this);
    },

    jump: function() {
       
        if (game.paused){
            requestStart();
            go.text = "Detecting face...";
        }
        
        this.bird.body.velocity.y = -350;
    },

    addOnePipe: function(x, y) {
        var pipe = game.add.sprite(x, y, 'pipe');

        this.pipes.add(pipe);
        game.physics.arcade.enable(pipe);
        pipe.body.velocity.x = -200; 
        pipe.checkWorldBounds = true;
        pipe.outOfBoundsKill = true;
    },

    addRowOfPipes: function() {
        var hole = Math.floor(Math.random() * 5) + 1;

        for (var i = 0; i < 8; i++)
            if (i != hole && i != hole + 1) 
                this.addOnePipe(400, i * 60 + 10);   

        this.score += 1;
        this.labelScore.text = this.score;
        score = this.score;
    },

    restartGame: function() {
        reportActivity();
    },
};

function requestStart() {

    if (startRequested)
        return;
    startRequested = true;
    
    var data = {
            "cmd" : "startGame",
    };

    var ws = new WebSocket("ws://chepePixiePro.local:8001");

    ws.onopen = function() {
        msg = JSON.stringify(data);
        ws.send(msg);
    }

    ws.onmessage = function(evt) {
        var msg = evt.data;
        switch (msg) {

            case "Ok":
                data.cmd = "pollResponse";
                msg = JSON.stringify(data);
                setTimeout(function() { ws.send(msg)}, 1000);
                break;

            case "Start":
                ws.close();
                break;

            default:
            break;
        }  
    }

    ws.onclose = function() {
        go.destroy();
        game.paused = false;
        }
}
    
function reportActivity() {
    var d = new Date();
    var n = d.toUTCString();
    var data = {

            "score" : score,
            "cmd" : "stopGame",
            "date" : n
    };

    if (stopRequested) {
        return;
    }
    stopRequested = true;
    
    var ws = new WebSocket("ws://chepePixiePro.local:8001");

    ws.onopen = function() {
        msg = JSON.stringify(data);
        ws.send(msg);
    }

    ws.onmessage = function(evt) {
        var msg = evt.data;
        ws.close()
        
    }

    ws.onclose = function() {
        game.state.start('main');
        }
}

var game = new Phaser.Game(400, 490);
game.state.add('main', mainState, true); 
