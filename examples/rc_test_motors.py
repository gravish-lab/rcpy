if __name__ == "__main__":

    # This is only necessary if package has not been installed
    import sys
    sys.path.append('..')

# import python libraries
import time
import getopt

# import rc library
# This automatically initizalizes the robotics cape
import rc 
import rc.motor as motor

def usage():
    print("""usage: python rc_test_motors [options] ...
Options are:
-d duty     define a duty cycle from -1.0 to 1.0
-m motor    specify a single motor from 1-4, 0 for all motors
-s          sweep motors back and forward at duty cycle
-b          enable motor brake function
-f          enable free spin function
-h          print this help message""")

def main():

    # exit if no options
    if len(sys.argv) < 2:
        usage()
        sys.exit(2)
    
    # Parse command line
    try:
        opts, args = getopt.getopt(sys.argv[1:], "bfhsd:m:", ["help"])

    except getopt.GetoptError as err:
        # print help information and exit:
        print('rc_test_motors: illegal option {}'.format(sys.argv[1:]))
        usage()
        sys.exit(2)

    # defaults
    duty = 0.0
    channel = 0
    sweep = False
    brk = False
    free = False

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in "-d":
            duty = float(a)
        elif o in "-m":
            channel = int(a)
        elif o == "-s":
            sweep = True
        elif o == "-b":
            brk = True
        elif o == "-f":
            free = True
        else:
            assert False, "Unhandled option"

    try:

        # set state to rc.RUNNING
        rc.set_state(rc.RUNNING);

        # set motor duty (only one option at a time)
        if brk:
            print('Breaking motor {}'.format(channel))
            motor.set_brake(channel)
            sweep = False
        elif free:
            print('Setting motor {} free'.format(channel))
            motor.set_free_spin(channel)
            sweep = False
        elif duty != 0:
            if not sweep:
                print('Setting motor {} to {} duty'.format(channel, duty))
                motor.set(channel, duty)
            else:
                print('Sweeping motor {} to {} duty'.format(channel, duty))
        else:
            sweep = False

        # message
        print("Press Ctrl-C to exit");
        
        # sweep
        if sweep:

            d = 0
            direction = 1
            delta = duty/20
            
            # keep running
            while rc.get_state() != rc.EXITING:

                # running
                if rc.get_state() == rc.RUNNING:

                    # increment duty
                    d = d + direction * delta
                    motor.set(channel, d)

                    # end of range?
                    if d > duty or d < -duty:
                        direction = direction * -1
                        
                elif rc.get_state() == rc.PAUSED:

                    # set motors to free spin
                    motor.set_free_spin(channel)
                    d = 0
                    
                # sleep some
                time.sleep(.1)

        # or do nothing
        else:

            # keep running
            while rc.get_state() != rc.EXITING:
                
                # sleep some
                time.sleep(1)
            
    except (KeyboardInterrupt, SystemExit):
        # handle what to do when Ctrl-C was pressed
        pass
        
    finally:

        # say bye
        print("\nInterrupted.");
            
# exiting program will automatically clean up cape

if __name__ == "__main__":
    main()
