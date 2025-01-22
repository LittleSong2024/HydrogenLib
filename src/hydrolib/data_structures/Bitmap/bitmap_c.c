#include <math.h>
#include <stdlib.h>
#include <stdbool.h>

#define new(x) (x *)malloc(sizeof(x))
#define new_array(x, y) (x *)malloc(sizeof(x) * y)

struct Byte_t
{
    unsigned int bit1 : 1;
    unsigned int bit2 : 1;
    unsigned int bit3 : 1;
    unsigned int bit4 : 1;
    unsigned int bit5 : 1;
    unsigned int bit6 : 1;
    unsigned int bit7 : 1;
    unsigned int bit8 : 1;
};

void init_byte(struct Byte_t *byte){
    byte->bit1 = 0;
    byte->bit2 = 0;
    byte->bit3 = 0;
    byte->bit4 = 0;
    byte->bit5 = 0;
    byte->bit6 = 0;
    byte->bit7 = 0;
    byte->bit8 = 0;
}

struct Byte_t* new_byte(){
    struct Byte_t *byte = new (struct Byte_t);
    init_byte(byte);
    return byte;
}

struct Bitmap_t
{
    struct Byte_t* data;
    int size;
};

struct Bitmap_t *create_bitmap(int size)
{
    struct Bitmap_t *bitmap = new (struct Bitmap_t);
    bitmap->data = new_array(struct Byte_t, size);
    bitmap->size = size;
    return bitmap;
}

void init_bitmap(struct Bitmap_t *bitmap)
{
    for (int i = 0; i < bitmap->size; i++)
    {
        init_byte(&bitmap->data[i]);
    }
}

bool set_bit(struct Bitmap_t *bitmap, int index, int value)
{
    int byte_index = index / 8;
    int bit_index = index % 8;
    if (byte_index >= bitmap->size){
        return false;
    }
    switch (bit_index)
    {
    case 0:
        bitmap->data[byte_index].bit1;
        break;

    case 1:
        bitmap->data[byte_index].bit2;
        break;

    case 2:
        bitmap->data[byte_index].bit3;
        break;

    case 3:
        bitmap->data[byte_index].bit4;
        break;

    case 4:
        bitmap->data[byte_index].bit5;
        break;

    case 5:
        bitmap->data[byte_index].bit6;
        break;

    case 6:
        bitmap->data[byte_index].bit7;
        break;

    case 7:
        bitmap->data[byte_index].bit8;
        break;

    default:
        break;
    }
    return true;
}

bool get_bit(struct Bitmap_t *bitmap, int index)
{
    int byte_index = index / 8;
    int bit_index = index % 8;
    if (byte_index >= bitmap->size){
        return false;
    }
    switch (bit_index)
    {
    case 0:
        return bitmap->data[byte_index].bit1;
        break;

    case 1:
        return bitmap->data[byte_index].bit2;
        break;

    case 2:
        return bitmap->data[byte_index].bit3;
        break;

    case 3:
        return bitmap->data[byte_index].bit4;
        break;

    case 4:
        return bitmap->data[byte_index].bit5;
        break;

    case 5:
        return bitmap->data[byte_index].bit6;
        break;

    case 6:
        return bitmap->data[byte_index].bit7;
        break;

    case 7:
        return bitmap->data[byte_index].bit8;
        break;

    default:
        break;
    }
}


void reset_data(struct Bitmap_t *bitmap, int size){
    free(bitmap->data);
    bitmap->data = new_array(struct Byte_t, size);
}
