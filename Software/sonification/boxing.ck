//Author: Santiago Hernandez & Gabe Rottet

// Define an array of string to hold your file paths
/*
string samples[];
*/

// Add your .wav file paths to the array
// Make sure to use forward slashes in the path, even on Windows

FileIO sound_dir;
me.dir() + "sound_files/" => string sound_file_path;
sound_dir.open(sound_file_path, FileIO.READ);
sound_dir.dirList() @=> string sound_files[];
string samples[sound_files.size()];
for (int i; i < sound_files.size(); i++){
    sound_file_path + sound_files[i] => samples[i];
}

sound_dir.close();

OscIn receiver;
8001 => int port;
if (!receiver.port(port)) <<< "ERROR Port Failed" >>>;
receiver.addAddress("/sonification");
receiver.listenAll();
OscMsg msg;

float data_reading[9];
// Seed the random number generator (optional, but good practice)
// Using now::ms as a seed ensures a different sequence each run
//now::ms() => Std.srandom;
2 => Math.srandom;

// Create a SndBuf object to load and play the audio
SndBuf buffer => LPF lpf => Bitcrusher crush => JCRev rev => dac;
1 => buffer.gain;
1 => rev.gain;
0.9 => crush.gain;

// Loop indefinitely to play random files
fun playRandomFile(float data[]) { 
    for (int i; i < data.size(); i++) {
        <<< data[i] >>>;
    }
    
    crush.bits((data[6] / 128) $ int);
    crush.downsampleFactor(1 + ((data[6]) $ int) / 1000);
        
    (80 - (((Std.fabs(data[0]) + Std.fabs(data[1]) + Std.fabs(data[2])) $ int) / 3)) / 80 => rev.mix;
    
    (20000 - ((6 - Std.fabs(data[5])) $ int) * 3333) => lpf.freq;      
    // Generate a random index between 0 and the last index of the array
    // Math.random2(min, max) generates an integer in the range [min, max]
    Math.random2(0, samples.size() - 1) => int randomIndex;

    // Get the random file path from the array
    samples[randomIndex] => string randomFile;
    
    // Load the randomly selected file into the buffer
    randomFile => buffer.read;

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

me.dir() + "sound_files/ambience_1.wav" => ambience_buffer0.read;
me.dir() + "sound_files/ambience_1_1.wav" => ambience_buffer1.read;
me.dir() + "sound_files/ambience_2_1.wav" => ambience_buffer2.read;
me.dir() + "sound_files/ambience_3_1.wav" => ambience_buffer3.read;

SndBuf ambience_buffers[4];
ambience_buffers[0] => ambience_buffer0;
ambience_buffers[1] => ambience_buffer1;
ambience_buffers[2] => ambience_buffer2;
ambience_buffers[3] => ambience_buffer3;

0.01 => rev0.mix;
0.01 => rev1.mix;
0.01 => rev2.mix;
0.01 => rev3.mix;

0.0 => rev0.gain;
0.0 => rev1.gain;
0.0 => rev2.gain;
0.0 => rev3.gain;

fun playAmbience(SndBuf buf) {        
   buf.samples() => buf.pos;
   0 => buf.pos;
   buf.length() => now;
} 

for (int i; i < ambience_buffers.size(); i++) {
    spork ~ playAmbience(ambience_buffers[i]);
}
while (true) {

    receiver => now;
    
    while (receiver.recv(msg)) {
        <<< "hit">>>;
        if (msg.address == "/sonification") { 
            for (int i; i < data_reading.size(); i++) {
                msg.getFloat(i) => data_reading[i];
            }
            spork ~ playRandomFile(data_reading);
        }
    }
}
