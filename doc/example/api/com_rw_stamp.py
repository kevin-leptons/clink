from clink.com import write_stamp, read_stamp


class BrokenCar():
    def boot(self):
        print('Oop!, something went wrong.')


write_stamp(BrokenCar, 'note', 'This cars can not boot. It must be fixs')
note = read_stamp(BrokenCar, 'note')


print('class BrokenCar has a note:', note)
