//Author: Santiago Hernandez & Gabe Rottet
// Add your .wav file paths to the array
// Make sure to use forward slashes in the path, even on Windows


/*
PunchID
ax,ay,az,gx,gy,gz,piezo,timestamp
ax,ay,az,gx,gy,gz
*/

FileIO sound_dir;
me.dir() + "sound_files/" => string sound_file_path;
sound_dir.open(sound_file_path, FileIO.READ);
sound_dir.dirList() @=> string sound_files[];

string ambience_sounds[0];
string cross_sounds[0];
string hook_sounds[0];
string jab_sounds[0];
string uppercut_sounds[0];
string bjab_sounds[0];
string wjab_sounds[0];
string sjab_sounds[0];
string scross_sounds[0];
string dinosaur_meteor[0];
string master_sounds[0];

//Sorts sound_files into each lsit
fun sortSounds() {
    
    int sizeHolder;
    
    for (int i; i < sound_files.size(); i++){
        
        if (sound_files[i].charAt2(0) == "S") {
            
            if (sound_files[i].charAt2(1) == "C") {
                scross_sounds.size() => sizeHolder;
                scross_sounds.size(sizeHolder + 1);
                sound_file_path + sound_files[i] => scross_sounds[sizeHolder];
            } else if (sound_files[i].charAt2(1) == "J") {
                sjab_sounds.size() => sizeHolder;
                sjab_sounds.size(sizeHolder + 1);
                sound_file_path + sound_files[i] => sjab_sounds[sizeHolder];
            }
            
        } else if (sound_files[i].charAt2(0) == "B") {
            
            bjab_sounds.size() => sizeHolder;
            bjab_sounds.size(sizeHolder + 1);
            sound_file_path + sound_files[i] => bjab_sounds[sizeHolder];        
        } else if (sound_files[i].charAt2(0) == "W") {
            
            wjab_sounds.size() => sizeHolder;
            wjab_sounds.size(sizeHolder + 1);
            sound_file_path + sound_files[i] => wjab_sounds[sizeHolder];
        
        } else if (sound_files[i].charAt2(0) == "A") {
            
            ambience_sounds.size() => sizeHolder;
            ambience_sounds.size(sizeHolder + 1);
            sound_file_path + sound_files[i] => ambience_sounds[sizeHolder];
            
        } else if (sound_files[i].charAt2(0) == "C") {
            
            cross_sounds.size() => sizeHolder;
            cross_sounds.size(sizeHolder + 1);
            sound_file_path + sound_files[i] => cross_sounds[sizeHolder];
        
        } else if (sound_files[i].charAt2(0) == "H") {
            
            hook_sounds.size() => sizeHolder;
            hook_sounds.size(sizeHolder + 1);
            sound_file_path + sound_files[i] => hook_sounds[sizeHolder];
        
        } else if (sound_files[i].charAt2(0) == "U") {
            
            uppercut_sounds.size() => sizeHolder;
            uppercut_sounds.size(sizeHolder + 1);
            sound_file_path + sound_files[i] => uppercut_sounds[sizeHolder];
        
        }
        
        master_sounds.size() => sizeHolder;
        master_sounds.size(sizeHolder + 1);
        sound_file_path + sound_files[i] => master_sounds[sizeHolder];
    }
}

sortSounds();

OscIn receiver;
8001 => int port;
if (!receiver.port(port)) <<< "ERROR Port Failed" >>>;
receiver.addAddress("/sonification");
receiver.listenAll();
OscMsg msg;

float data_reading[15];
// Seed the random number generator (optional, but good practice)
// Using now::ms as a seed ensures a different sequence each run
//now::ms() => Std.srandom;
2 => Math.srandom;

// Create a SndBuf object to load and play the audio
SndBuf buffer => Bitcrusher crush => dac;
LPF lpf => JCRev rev;

.5 => buffer.gain;
1 => rev.gain;
0 => rev.mix;
.2 => crush.gain;

fun float abs(float val, float center) {
    float relative;
    if (val > center) {
        val-center => relative;
    } else {
        center - val => relative;
    }
    
    if (relative > 0) {
        return relative;
    } else {
        return 0 - relative;
    }
}

fun bitcrush(float gx, float gy, float gz, float egx, float egy, float egz, float p) {
    abs(egx, 0) => egx;
    abs(egy, 0) => egy;
    abs(egz, 0) => egz;
    13 => float max_x;
    15 => float max_y;
    10 => float max_z;
    0 => float total;
    ((gx * ((.3 - 0) $ float / max_x)) + 0) $ float => float one;
    ((gy * ((.3 - 0) $ float / max_y)) + 0) $ float => float two;
    ((gz * ((.3 - 0) $ float / max_z)) + 0) $ float => float three;
    <<<one, two, three>>>;

    one + two + three => total;
    (p * (6.0 / 4095) + 4) $ int => int bitz;
    (total * 50) $ int => int dsf;
    if (dsf < 1) 1 => dsf;
    1 => dsf;
    crush.bits(bitz);
    crush.downsampleFactor(dsf);
  
    <<<"CRUSH_BITS: ", bitz>>>;
    <<<"CRUSH_DSF: ", dsf>>>;
}

fun lowpassfilter(float ax, float ay, float az, float eax, float eay, float eaz) {
    75000 => int limit;
    abs(eax, ax) => eax;
    abs(eay, ay) => eay;
    abs(eaz, az) => eaz;
    72 => float max_x;
    72 => float max_y;
    72 => float max_z;
    0 => float total;
    ((eax * ((.3 - 0) $ float / max_x)) + 0) $ float +=> total;
    ((eay * ((.3 - 0) $ float / max_y)) + 0) $ float +=> total;
    ((eaz * ((.3 - 0) $ float / max_z)) + 0) $ float +=> total;
    if (total > 1) {
        1 => total;
    }
    0 => total;
    limit - (total * limit) => float f => lpf.freq;
    <<<"LPF: ", f>>>;
}


fun reverb(float p) {
    ((p * ((1) $ float / 4095)) + 0) $ float => float r => rev.mix;
    <<<"REV: ", r>>>;
}

fun string getPunchById(float id) {
    if (id == 0) return "cross";
    else if (id == 1) return "jab";
    else if (id == 2) return "left_hook";
    else if (id == 3) return "right_hook";
    else if (id == 4) return "uppercut";
    else return "invalid_id";
}


string punch_id;

// Loop indefinitely to play random files
fun playRandomFile(float data[]) { 
    
    for (int i; i < data.size(); i++) {
        <<< data[i] >>>;
    }
    
    getPunchById(data[0]) => punch_id;
  
    bitcrush(data[4], data[5], data[6], -32.1785, 60.907,-36.046,data[7]);
    //lowpassfilter(data[1], data[2], data[3], 10.79 ,8.3085,11.835);
    //reverb(data[7]);
    // Generate a random index between 0 and the last index of the array
    // Math.random2(min, max) generates an integer in the range [min, max]
    Math.random2(0, master_sounds.size() - 1) => int randomIndex;

    // Get the random file path from the array
    master_sounds[randomIndex] => string randomFile;
    
    // Load the randomly selected file into the buffer
    randomFile => buffer.read;
    <<<randomFile>>>;
    1 => buffer.gain;

    // Play the file
    // Set position to the end of the buffer (buffer.samples() is total samples)
    buffer.samples() => buffer.pos;
    // Set position to 0 to start playback from the beginning
    0 => buffer.pos;
    
    // Wait for the duration of the sample before the next iteration
    // The "now" keyword advances time by the buffer length
    buffer.length() => now;
    
}

SndBuf ambience_buffer0 => NRev rev0 => dac;
SndBuf ambience_buffer1 => NRev rev1 => dac;
SndBuf ambience_buffer2 => NRev rev2 => dac;
SndBuf ambience_buffer3 => NRev rev3 => dac;

1 => ambience_buffer0.gain;


sound_file_path + "Ambience01.wav" => ambience_buffer0.read;
sound_file_path + "Ambience01.wav" => ambience_buffer1.read;
sound_file_path + "Ambience02.wav" => ambience_buffer2.read;
sound_file_path + "Ambience03.wav" => ambience_buffer3.read;

SndBuf ambience_buffers[4];
ambience_buffers[0] => ambience_buffer0;
ambience_buffers[1] => ambience_buffer1;
ambience_buffers[2] => ambience_buffer2;
ambience_buffers[3] => ambience_buffer3;

0.01 => rev0.mix;
0.01 => rev1.mix;
0.01 => rev2.mix;
0.01 => rev3.mix;
0.2 => rev0.gain;
0.2 => rev1.gain;
0.2 => rev2.gain;
0.2 => rev3.gain;

fun playAmbience(SndBuf buf) {
   while (true) {
       buf.samples() => buf.pos;
       0 => buf.pos;
       buf.length() => now;
   }
} 

for (int i; i < ambience_buffers.size(); i++) {
    spork ~ playAmbience(ambience_buffers[i]);
}

0 => float previous_timestamp;

while (true) {

    receiver => now;
    
    if (receiver.recv(msg)) {
        
        //Skips redundant packets
        while (msg.getFloat(8) == previous_timestamp) {
            receiver.recv(msg);
        }
        
        if (msg.address == "/sonification") { 
            for (int i; i < data_reading.size(); i++) {
                msg.getFloat(i) => data_reading[i];
            }
            spork ~ playRandomFile(data_reading);
        }
        msg.getFloat(8) => previous_timestamp;
    }
}
