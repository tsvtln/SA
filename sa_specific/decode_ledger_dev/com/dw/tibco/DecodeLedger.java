

package com.dw.tibco;

import com.dw.tibco.proto.Util;
import com.dw.tibco.proto.types.*;
import com.dw.tibco.ledger.LedgerDecoder;
import com.dw.tibco.ledger.Entry;

import java.io.File;
import java.io.InputStream;

/**
 * This program parses tibco ledger files.  Ledger files are composed of 
 * arbitrary length entries.  These entries are 512 byte aligned.  Each entry
 * has a 36 byte header followed by a dictionary record.  A dictionary record
 * is composed of a list of key/value pairs.  The keys are simple length-value
 * strings.  The values are encoded as type-length-value.
 *
 * Known datatypes are:
 * 01 - dictionary
 * 02 - string array
 *        <num_elements> <el1_len> <el1_str> <el2_len> <el2_str> ...
 *      where the lenth of each element includes the length specifier.
 * 07 - binary blob
 * 08 - string
 * 0c - unsigned integer
 *
 * BERish length encoding:
 * 1-byte: XX             (exclusive)
 * 2-byte: 79 XX XX       (inclusive)
 * 4-byte: 7a XX XX XX XX (inclusive)
-------------------------------------------------------------------------------

SECTOR_LEN = 512

DICT_MAGIC = "\x99\x55\xee\xaa"

ENTRY_HEAD_LEN = 36

# A record is composed of key/value pairs.
# A key has form: <len> <key>
# A value has the form: <type> <len> <value>
 */

// toString() gives a complete verbose representation of the data.
// pPrint() Gives a terse "human readable" representation of the data.

public class DecodeLedger {
    // Decodes and prints the entries in the ledger file given by <fileLedger>.
    private static void decodeLedger(File fileLedger, boolean bVerbose) {
        // Let user know which ledger file we are decoding.
        System.out.println(fileLedger.getName() + ":");

        // Create a ledger decoder for this ledger file.
        LedgerDecoder ledgerDec = new LedgerDecoder(fileLedger);

        // Get the first entry out of this ledger file.
        Entry curEntry = ledgerDec.nextEntry();

        // As long as we continue to have a ledger entry.
        while (curEntry != null) {
            if ( bVerbose ) {
                System.out.println(curEntry.toString());
            } else {
                System.out.println(curEntry.pPrint());
            }
        }
    }

    /*
     *  Usage: cmd [-v] [<ledgerfile1> <ledgerfile2> ...]
     */
    public static void main( String[] asArgs ) {
        // Whether or not to output verbose formatting.
        boolean bVerbose = false;

        // Itterate through all the arguments.
        for ( int iCurArg = 0; iCurArg < asArgs.length; iCurArg++ ) {
            String sCurArg = asArgs[iCurArg];

            if (sCurArg == "-v") {
                bVerbose = true;
            } else {
                decodeLedger(new File(sCurArg), bVerbose);
            }
        }

        System.out.println("Hello: " + (byte)0xff);
    }
}
