#include <Python.h>
#include <math.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>

#define new(x) (x *)malloc(sizeof(x))
#define new_array(x, y) (x *)malloc(sizeof(x) * y)

#define ll long long
#define ull unsigned long long

typedef struct {
    PyObject_HEAD

    unsigned int bit1 : 1;
    unsigned int bit2 : 1;
    unsigned int bit3 : 1;
    unsigned int bit4 : 1;
    unsigned int bit5 : 1;
    unsigned int bit6 : 1;
    unsigned int bit7 : 1;
    unsigned int bit8 : 1;
} Byte_t;

typedef struct {
    PyObject_HEAD

    Byte_t* data;
    ull size;

} BitmapObject;

static void init_byte(Byte_t *byte) {
    byte->bit1 = 0;
    byte->bit2 = 0;
    byte->bit3 = 0;
    byte->bit4 = 0;
    byte->bit5 = 0;
    byte->bit6 = 0;
    byte->bit7 = 0;
    byte->bit8 = 0;
}


static void _byte_set_bit(Byte_t *byte, int bit_index, int value){
    switch(bit_index){
        case 0: byte->bit1 = value; break;
        case 1: byte->bit2 = value; break;
        case 2: byte->bit3 = value; break;
        case 3: byte->bit4 = value; break;
        case 4: byte->bit5 = value; break;
        case 5: byte->bit6 = value; break;
        case 6: byte->bit7 = value; break;
       case 7: byte->bit8 = value; break;
    }
}

static int _byte_get_bit(Byte_t* byte, ull bit_index){
    switch(bit_index){
        case 0: return byte->bit1;
        case 1: return byte->bit2;
        case 2: return byte->bit3;
        case 3: return byte->bit4;
        case 4: return byte->bit5;
        case 5: return byte->bit6;
        case 6: return byte->bit7;
        case 7: return byte->bit8;
    }
}

static int _byte_to_int(Byte_t *byte){
    return (
        ((int)(byte->bit1)) |
        (((int)(byte->bit2)) << 1) |
        (((int)(byte->bit3)) << 2) |
        (((int)(byte->bit4)) << 3) |
        (((int)(byte->bit5)) << 4) |
        (((int)(byte->bit6)) << 5) |
        (((int)(byte->bit7)) << 6) |
        (((int)(byte->bit8)) << 7));
}


bool check_index(ull num, ull start, ull end){
    return (num >= start && num < end);
}


static void _bitmap_set_bit(BitmapObject *bitmap, ull index, bool on){
    ull byte_index = index / 8;
    ull bit_index = index % 8;
    _byte_set_bit(&(bitmap->data[byte_index]), bit_index, on);
}

static int _bitmap_get_bit(BitmapObject *bitmap, ull index){
    ull byte_index = index / 8;
    ull bit_index = index % 8;
    return _byte_get_bit(&(bitmap->data[byte_index]), bit_index);
}

static void _bitmap_set_bits(BitmapObject *bitmap, int on, ull start, ull end, ull step){
    for (ull i = start; i < end; i += step){
        _bitmap_set_bit(bitmap, i, on);
    }
}

ull _get_range_length(ull start, ull end, ull step){
    if (start == end)return 0;
    if (start < end && step < 0)return 0;
    if (step == 0)return 0;
    if(step > 0)return max(0, (end - start - 1) / step + 1);
    else if (step < 0)return max(0, (end - start + 1) / step + 1);
}

int* _bitmap_get_bits(BitmapObject *bitmap, ull start, ull end, ull step){
    if (start == end){
        return NULL;
    }
    ull length = _get_range_length(start, end, step);
    int* bits = new_array(int, length);
    for(ull i = start; i < end; i += step){
        bits[i - start] = _bitmap_get_bit(bitmap, i);
    }
}

int _bitmap_get_byte(BitmapObject *bitmap, ull index){
    ull byte_index = index / 8;
    Byte_t* byte = &bitmap->data[byte_index];
    
}

int* _bitmap_to_bytes(BitmapObject *bitmap){
    int* bytes = new_array(int, bitmap->size);
    for(int i = 0;i < bitmap->size;i++){
        bytes[i] = _byte_to_int(&bitmap->data[i]);
    }
    return bytes;
}

