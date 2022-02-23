# Header formatting an codes
PKT_HEADER_FMT = ">BBHBBHIIQ"

HEADER_LEN = 24

REQ_MAGIC = 0x80
RES_MAGIC = 0x81

# DCP command opcodes # Hex # Dec
CMD_OPEN             = 0x50 # 80
CMD_ADD_STREAM       = 0x51 # 81
CMD_CLOSE_STREAM     = 0x52 # 82
CMD_STREAM_REQ       = 0x53 # 83
CMD_GET_FAILOVER_LOG = 0x54 # 84
CMD_STREAM_END       = 0x55 # 85
CMD_SNAPSHOT_MARKER  = 0x56 # 86
CMD_MUTATION         = 0x57 # 87
CMD_DELETION         = 0x58 # 88
CMD_EXPIRATION       = 0x59 # 89
CMD_FLUSH            = 0x5a # 90
CMD_SET_VB_STATE     = 0x5b # 91

# Memcached command opcodes

CMD_SET               = 0x01 # 1
CMD_DELETE            = 0x04 # 4
CMD_FLUSH             = 0x08 # 8
CMD_STATS             = 0x10 # 16
CMD_SASL_AUTH         = 0x21 # 33
CMD_STOP_PERSISTENCE  = 0x80 # 128
CMD_START_PERSISTENCE = 0x81 # 129

# Flag values
FLAG_OPEN_CONSUMER = 0x00
FLAG_OPEN_PRODUCER = 0x01

# Error Codes
SUCCESS             = 0x00 # 0
ERR_KEY_ENOENT      = 0x01 # 1
ERR_KEY_EEXISTS     = 0x02 # 2
ERR_E2BIG           = 0x03 # 3
ERR_EINVAL          = 0x04 # 4
ERR_NOT_STORED      = 0x05 # 5
ERR_DELTA_BADVAL    = 0x06 # 6
ERR_NOT_MY_VBUCKET  = 0x07 # 7
ERR_AUTH_ERROR      = 0x20 # 32
ERR_AUTH_CONTINUE   = 0x21 # 33
ERR_ERANGE          = 0x22 # 34
ERR_ROLLBACK        = 0x23 # 35
ERR_UNKNOWN_COMMAND = 0x81 # 129
ERR_ENOMEM          = 0x82 # 130
ERR_NOT_SUPPORTED   = 0x83 # 131
ERR_EINTERNAL       = 0x84 # 132
ERR_EBUSY           = 0x85 # 133
ERR_ETMPFAIL        = 0x86 # 134
ERR_ECLIENT         = 0xff # 255
