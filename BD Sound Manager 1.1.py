import argparse
import os
import sys
import struct
import subprocess
import time
parser = argparse.ArgumentParser()
parser.add_argument("-bd", "--bd", help=".BD File")
parser.add_argument("-hd", "--hd", help=".HD File")
parser.add_argument("-o", "--out", help="Output folder (must exist)")
parser.add_argument("-inf", "--inputfolder", help="Input folder (must exist)")
parser.add_argument("-in", "--input", help="Input VAG file for export")
parser.add_argument("-m", "--mode", help="'E' For extract, 'i' For import, 'F' for fix VAG file, 'l' for list audio in BD file")
args = parser.parse_args()
if args.mode == None:
    if args.bd == None or args.hd == None:
        print ("""
    BD Sound Manager v.1.1
    (for Parappa The Rapper 2)
    Version 1.1
    Original code by Nisto
    Modificated programm by Yan4ik
    
    For help, please type -h
    Please run programm always in CMD
        """)
        time.sleep(5)
        quit()
def fixvag (file):
    # By Yan4ik / Original code by pips
    # read file from buffer
    data = file.read()
    # find index
    i = data.find(b"\x00\x07\x77\x77\x77\x77\x77\x77\x77\x77\x77\x77\x77\x77\x77\x77")
    if i == -1:
        print("Unknown VAG file.")
    else:
        # seek to byte
        buffer = file.read(file.seek(i - 15))
        bdfixedtest = buffer.find(b'\x01')
        if bdfixedtest == -1:
          file.seek(i - 15)
          file.write(b"\x01")
          print('VAG Fixed!')
        else:
        	print('Already fixed!')
if args.mode == 'f':
    in_vag_path = args.input
    if not os.access(in_vag_path, os.R_OK):
        print("Could not open .VAG file")
        sys.exit(1)
    with open(in_vag_path, "rb+") as in_vagf:
      fixvag(in_vagf)
    exit();
def get_u16_le(buf, offset):
    return struct.unpack("<H", buf[offset:offset+2])[0]

def get_u16_be(buf, offset):
    return struct.unpack(">H", buf[offset:offset+2])[0]

def get_u32_le(buf, offset):
    return struct.unpack("<I", buf[offset:offset+4])[0]

def get_u32_be(buf, offset):
    return struct.unpack(">I", buf[offset:offset+4])[0]

def put_u16_le(buf, offset, value):
    buf[offset:offset+2] = struct.pack("<H", value)

def put_u16_be(buf, offset, value):
    buf[offset:offset+2] = struct.pack(">H", value)

def put_u32_le(buf, offset, value):
    buf[offset:offset+4] = struct.pack("<I", value)

def put_u32_be(buf, offset, value):
    buf[offset:offset+4] = struct.pack(">I", value)

def get_vag_param_offset(hdbuf, vagi_chunk_offset, index):
    return get_u32_le(hdbuf, vagi_chunk_offset + 0x10 + (index * 4))

def get_vag_offset(hdbuf, vagi_chunk_offset, index):
    return get_u32_le(hdbuf, vagi_chunk_offset + get_vag_param_offset(hdbuf, vagi_chunk_offset, index) + 0x00)

def get_vag_sample_rate(hdbuf, vagi_chunk_offset, index):
    return get_u16_le(hdbuf, vagi_chunk_offset + get_vag_param_offset(hdbuf, vagi_chunk_offset, index) + 0x04)

def put_vag_offset(hdbuf, vagi_chunk_offset, index, vag_offset):
    put_u32_le(hdbuf, vagi_chunk_offset + get_vag_param_offset(hdbuf, vagi_chunk_offset, index) + 0x00, vag_offset)

def put_vag_sample_rate(hdbuf, vagi_chunk_offset, index, sample_rate):
    put_u16_le(hdbuf, vagi_chunk_offset + get_vag_param_offset(hdbuf, vagi_chunk_offset, index) + 0x04, sample_rate)

def isnum(n):
    try:
        int(n)
    except ValueError:
        return False
    return True

def get_file_arg(message, real=True):
    x = ''
    while not os.path.isfile(x):
        x = input(message).strip('"')
    return os.path.realpath(x)

def get_dir_arg(message, real=True):
    x = ''
    while not os.path.isdir(x):
        x = input(message).strip('"')
    return os.path.realpath(x)

def get_num_arg(message, negative=False):
    x = ''
    while not isnum(x) or (not negative and int(x) < 0):
        x = input(message)
    return int(x)

def get_lit_arg(valid_list, message, lowercase=True):
    x = ''
    while x not in valid_list:
        x = input(message)
        if lowercase:
            x = x.lower()
    return x
mode = args.mode
hd_path = args.hd
bd_path = args.bd
if not os.access(bd_path, os.R_OK):
    print("Could not open .BD file")
    sys.exit(1)
if not os.access(hd_path, os.R_OK):
    print("Could not open .HD file")
    sys.exit(1)
with open(hd_path, "rb") as hd:
    hdbuf = bytearray( hd.read() )

with open(bd_path, "rb") as bd:
    bdbuf = bytearray( bd.read() )
if hdbuf[0x00:0x08] != b"IECSsreV":
    print("Unexpected ID at 0x00 in .HD")

if hdbuf[0x10:0x18] != b"IECSdaeH":
    print("Unexpected ID at 0x10 in .HD")

bd_size = get_u32_le(hdbuf, 0x20)

vagi_chunk_offset = get_u32_le(hdbuf, 0x30)

max_vag_index = get_u32_le(hdbuf, vagi_chunk_offset + 0x0C)

if mode == 'e':
    out_dir = args.out
    if not os.access(out_dir, os.W_OK):
        print("Can not write to the specified folder!")
        sys.exit(1)

    bd_stem = os.path.splitext(bd_path)[0]

    bd_basename = os.path.basename(bd_stem)

    out_stem = os.path.join(out_dir, bd_basename)

    for vag_index in range(max_vag_index+1):
        vag_offset = get_vag_offset(hdbuf, vagi_chunk_offset, vag_index)

        if vag_index < max_vag_index:
            vag_size = get_vag_offset(hdbuf, vagi_chunk_offset, vag_index+1) - vag_offset
        else:
            vag_size = bd_size - vag_offset

        sample_rate = get_vag_sample_rate(hdbuf, vagi_chunk_offset, vag_index)

        header = bytearray(0x30)
        header[0x00:0x04] = b"VAGp"
        put_u32_be(header, 0x04, 0x20)
        put_u32_be(header, 0x0C, vag_size)
        put_u32_be(header, 0x10, sample_rate)

        with open("%s_%02d.VAG" % (out_stem, vag_index), "wb") as vag:
            vag.write(header + bdbuf[vag_offset:vag_offset+vag_size])
        ifilepath = "\"%s_%02d.VAG\"" % (out_stem, vag_index)
        efilepath = "\"%s_%02d.wav\"" % (out_stem, vag_index)
        args = " /OTWAVU /OF48000 /IF24000 " + ifilepath + " " + efilepath
        print("Converting file | MFAudio v.1.0", end="")
        subprocess.call("mfaudio " + args)
        print("Done.")
        os.remove("%s_%02d.VAG"% (out_stem, vag_index)) 
elif mode == 'i':
    in_dir = args.inputfolder
    hd_path = args.hd
    bd_path = args.bd
    if not os.access(in_dir, os.R_OK):
        input("Can not read the specified folder!")
        sys.exit(1)
    directory = os.fsencode(in_dir)
    target_vag_index = 0
    for file in os.listdir(directory):
        if os.path.splitext(file)[1] == b".wav":
          with open(hd_path, "rb") as hd:
              hdbuf = bytearray( hd.read() )

          with open(bd_path, "rb") as bd:
              bdbuf = bytearray( bd.read() )
        
          bd_size = get_u32_le(hdbuf, 0x20)
          vagi_chunk_offset = get_u32_le(hdbuf, 0x30)
          max_vag_index = get_u32_le(hdbuf, vagi_chunk_offset + 0x0C)
        
          filename = os.fsdecode(file)
          ifilepath = "\"%s\"" % (os.path.join(in_dir, filename))
          efilepath = "\"%s_%02d.VAG\"" % (os.path.join(in_dir, os.path.splitext(filename)[0]), target_vag_index)
          args = " /OTVAGC /OF24000 " + ifilepath + " " + efilepath
          print("Converting file | MFAudio v.1.0 ...", end="")
          subprocess.call("mfaudio " + args)
          print("Done. \nExecuting BD Fix v.1.1 :")
          in_vag_path = os.path.join(in_dir, os.path.splitext(filename)[0]) + "_%02d.VAG" % (target_vag_index)
          needle = b"\x00\x07\x77\x77\x77\x77\x77\x77\x77\x77\x77\x77\x77\x77\x77\x77"

          with open(in_vag_path, "rb+") as file:
            data = file.read()
    
            i = 0
            while True:
              i = data.find(needle, i)
              if i == -1:
                  break
        
              file.seek(i - 15)
              if file.peek(1) != b"\x01":
                  file.write(b"\x01")
                  print('Writed 1 flag | BD Fix v.1.1')

              i += 1
        
          #print(in_vag_path)
        
          with open(in_vag_path, "rb") as in_vagf:
              in_vag_header = in_vagf.read(0x30)
              # body_size = get_u32_be(in_vag_buf, 0x0C)
              in_vag_rate = get_u32_be(in_vag_header, 0x10)
              in_adpcm_buf = in_vagf.read()
        

          in_adpcm_size = len(in_adpcm_buf)

          if target_vag_index > max_vag_index:
              input("Specified sample index exceeds max index: ")
              sys.exit(1)

          target_vag_offset = get_vag_offset(hdbuf, vagi_chunk_offset, target_vag_index)
          if target_vag_index < max_vag_index:
              target_vag_size = get_vag_offset(hdbuf, vagi_chunk_offset, target_vag_index+1) - target_vag_offset
          else:
              target_vag_size = bd_size - target_vag_offset

          # update sample rate
          put_vag_sample_rate(hdbuf, vagi_chunk_offset, target_vag_index, in_vag_rate)

          # update offsets for subsequent samples
          for sub_vag_index in range(target_vag_index+1, max_vag_index+1):
              sub_vag_offset = get_vag_offset(hdbuf, vagi_chunk_offset, sub_vag_index)
              put_vag_offset(hdbuf, vagi_chunk_offset, sub_vag_index, (sub_vag_offset - target_vag_size) + in_adpcm_size)

          # update BD size
          put_u32_le(hdbuf, 0x20, (bd_size - target_vag_size) + in_adpcm_size)

          with open(hd_path, "wb") as hd:
              hd.write(hdbuf)

          with open(bd_path, "wb") as bd:
              bd.write(bdbuf[:target_vag_offset])
              bd.write(in_adpcm_buf)
              bd.write(bdbuf[target_vag_offset+target_vag_size:bd_size])
              bd.truncate()
        
          print("Successfully injected " + filename + " at bd index: " + str(target_vag_index))
          target_vag_index += 1
          os.remove(in_vag_path)
elif args.mode == 'l':
    bd_stem = os.path.splitext(bd_path)[0]

    bd_basename = os.path.basename(bd_stem)

    for vag_index in range(max_vag_index+1):
        vag_offset = get_vag_offset(hdbuf, vagi_chunk_offset, vag_index)

        if vag_index < max_vag_index:
            vag_size = get_vag_offset(hdbuf, vagi_chunk_offset, vag_index+1) - vag_offset
        else:
            vag_size = bd_size - vag_offset

        sample_rate = get_vag_sample_rate(hdbuf, vagi_chunk_offset, vag_index)

        header = bytearray(0x30)
        header[0x00:0x04] = b"VAGp"
        put_u32_be(header, 0x04, 0x20)
        put_u32_be(header, 0x0C, vag_size)
        put_u32_be(header, 0x10, sample_rate)
        bdstructure = bd_basename + '_' , vag_index
        if vag_index > 9:
            print ("{}{}{}".format(bd_basename,"_",vag_index))
        else:
            print ("{}{}{}{}".format(bd_basename,"_",0,vag_index))
 
print ('''
Done! 
BD Sound Manager v.1.1
Mod by Yan4ik
Original code by Nisto

Original code BDFix by pips
''')
quit()