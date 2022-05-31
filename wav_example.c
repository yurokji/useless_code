/* 학교종이 땡땡땡 WAV 파일 만들기 */

#include <stdio.h>
#include <math.h>
#include <stdlib.h>

const int sampleRate = 44100;
const int bitDepth = 16;
const int compression_code = 1;
const int channels = 1;

const float C4 = 261.63;
const float D4 = 293.66;
const float E4 = 329.63;
const float F4 = 349.23;
const float G4 = 392.00;
const float A4 = 440.00;
const float B4 = 493.88;

const float C5 = 523.25;
const float D5 = 587.33;
const float E5 = 659.25;
const float F5 = 698.46;
const float G5 = 783.99;
const float A5 = 880.00;
const float B5 = 987.77;
const float C6 = 1046.50;
const float NONE = 0;

const int bpm = 120;

// BPM에 맞춰 샘플의 양을 결정하는 코드
float noteDuration(float note_type)
{
    return note_type * (60.f/(float)bpm);
}

// 사인 파형 곡선 구조체
typedef struct SineWave
{
    float freq;
    float amp;
    float radian;
    float step;
} SineWave;

// 사인파형 샘플러
float sample_sine(SineWave* sw)
{
    float sample = sw->amp * sin(sw->radian);
    sw->radian += sw->step;
    return sample;

} 

int main() {
    
    FILE *fptr;
    short* data1 = NULL;
    short* data2 = NULL; 
    fptr = fopen("school_bell.wav", "wb");
    if (fptr == NULL)
    {
        printf("Error");
        exit(1);
    }

    //헤더 청크
    fprintf(fptr, "%s", "RIFF");
    fprintf(fptr, "%s", "----");
    fprintf(fptr, "%s", "WAVE");

    //포멧 청크
    fprintf(fptr, "%s", "fmt ");
    fwrite(&bitDepth, 4, 1, fptr); //Size
    fwrite(&compression_code, 2, 1, fptr); //Compression code
    fwrite(&channels, 2, 1, fptr); // Number of channels
    fwrite(&sampleRate, 4, 1, fptr); //Size
    int byteSampleRate = sampleRate * bitDepth / 8;
    fwrite(&byteSampleRate, 4, 1, fptr); // Byte Rate
    int blockAlign = bitDepth / 2;
    fwrite(&blockAlign, 2, 1, fptr); //Block align  
    fwrite(&bitDepth, 2, 1, fptr); //bitDepth

    // Data 청크
    fprintf(fptr, "%s", "data");
    fprintf(fptr, "%s", "----");
    int pos_before_wav_data = ftell(fptr);
    float maxamp = pow(2, bitDepth - 1) - 1;
    
    SineWave sinewave;


    // 학교종이 땡땡땡 메인 멜로디 부분
    // NONE: 묵음
    float notes[] = {NONE,NONE,NONE,NONE,
                     NONE,NONE,NONE,NONE,
                     G5, G5, A5, A5, G5, G5, E5, 
                     G5, G5, E5, E5, D5, NONE, 
                     G5, G5, A5, A5, G5, G5, E5, 
                     G5, E5, D5, E5, C5, NONE};
    float types[] = {1, 1, 1, 1, 
                     1, 1, 1, 1, 
                     1, 1, 1, 1, 
                     1, 1, 2, 
                     1, 1, 1, 1, 3, 1,
                     1, 1, 1, 1, 1, 1, 2, 
                     1, 1, 1, 1, 3, 1};

    
    size_t num_notes = sizeof(notes) / sizeof(notes[0]);
    size_t num_types = sizeof(types) / sizeof(types[0]);
    int amount_note = 0;
    for(int i=0; i < num_types; i++) 
        amount_note += types[i];

    size_t total_num_samples = 0;

    for (int k=0; k < num_notes; k++)
        total_num_samples += sampleRate * noteDuration(types[k]);
    
    data1 = malloc(total_num_samples * sizeof(short) * 4);

    float duration = 1;
    int count  = 0;
    for (int k=0; k < num_notes; k++)
    {
        sinewave.amp = 0.5f;
        sinewave.radian = 0.f;
        sinewave.freq = notes[k];
        sinewave.step = 2 * M_PI * sinewave.freq / sampleRate;
        float duration = noteDuration(types[k]);
        
        float maxamp = pow(2, bitDepth - 1) - 1;
        float sample;
        for(int i= 0 ; i < sampleRate * duration; i++) 
        {
                sample = sample_sine(&sinewave);
                int intSample = (int) (sample  * maxamp);
                short low = (short) intSample;
                *(data1 + count)= low;
                count++;
        }

    }


    // 반주 부분
    float notes2[] = {C4, G4, E4, G4};
    size_t total_num_samples2 = 0;
    for (int k=0; k < amount_note*2; k++)
        total_num_samples2 += sampleRate * noteDuration(0.5);
    count  = 0;
    printf("total_num_samples2: %d\n", total_num_samples2);
    data2 = malloc(total_num_samples2 * sizeof(short) * 8);
    for (int k=0; k < amount_note*2; k++)
    {
        sinewave.amp = 0.5f;
        sinewave.radian = 0.f;
        sinewave.freq = notes2[k % 4];
        sinewave.step = 2 * M_PI * sinewave.freq / sampleRate;
        float duration = noteDuration(0.5);
        // printf("%f\n", duration);
        float maxamp = pow(2, bitDepth - 1) - 1;
        float sample;
        for(int i= 0 ; i < sampleRate * duration; i++) 
        {
                sample = sample_sine(&sinewave);
                int intSample = (int) (sample  * maxamp);
                short low = (short) intSample;
                *(data2 + count)= low;
                count++;
        }
    }

    // 메인 멜로디와 반주 부분의 샘플을 합해준다
    for (int k=0; k < total_num_samples2; k++)
    {
        int sample_combined = data1[k]+data2[k];
        fwrite(&sample_combined, 2, 1, fptr);
    }

    //데이터 사이즈 구해서 채워넣기
    int pos_after_wav_data = ftell(fptr);
    fseek(fptr, pos_before_wav_data - 4, SEEK_CUR);
    int data_size = pos_after_wav_data  - pos_before_wav_data;
    fwrite(&data_size, 4, 1, fptr);

    // 파일 전체 사이즈에서 청크 아이디와 청크 사이즈를 제외한 값
    fseek(fptr, 4, SEEK_SET);
    int total_size = pos_after_wav_data - 8;
    fwrite(&total_size, 4, 1, fptr);
    printf("%d %d\n", data_size, total_size);
    fclose(fptr);
    return 0;
}
