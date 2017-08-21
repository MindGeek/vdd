# encoding=utf-8
import os.path
import random
import sys
import time

import simplejson as json

import config
import voice


class Learner:
    """
     听写单词的小工具
    """

    def __init__(self, filename='./vocab_db.json'):
        """

        :param filename: 本地存储单词 db 的路径
        """
        self.filename = filename
        self.vocabs = []
        self.vocabs_index = []

        self.goal_times = 0
        self.goal_peroid = 0

        self.words_showed = 0
        self.words_mistype = 0
        self.time_start = 0
        self.time_end = 0

        self.mod = 'deliberate'
        self.fail_rate_sum = 0
        self.short_memory_count = 10  # right 后 多少次之内不再出现
        self.short_memory = set()

    def set_goal(self):
        """
        设置本次练习的目标
        :return:
        """
        print '''
            输入本次练习的单词总数，或希望练习持续的时间
            例如: 20 min （如果你想练习20分钟） 或者  50 words（如果你想一共练习50个单词）
        '''
        goal = raw_input("What do you suppose me to do? ")
        if len(goal.split(' ')) == 1:
            num = goal
            self.goal_times = int(num)
            print 'okay, we will try %d words this time' % self.goal_times
        else:
            num, type = goal.split(' ')
            if type == 'min' or type == 'mins':
                self.goal_peroid = int(num)
                print 'yeah, we will do %d mins this time' % self.goal_peroid
            else:
                self.goal_times = int(num)
                print 'okay, we will try %d words this time' % self.goal_times
        self.time_start = time.time()

    def is_goal_reached(self):
        """

        :return:
        """
        if self.goal_peroid > 0:
            if time.time() > self.time_start + self.goal_peroid * 60:
                return True
        elif self.goal_times > 0:
            if self.goal_times <= self.words_showed:
                return True
        return False

    def get_word_fail_rate(self, item):
        """

        :param item:
        :return:
        """
        return (item[2] + 1) * 1.0 / (item[1] + 1)

    def sort_vocabs_if_needed(self):
        """

        :return:
        """
        if self.words_showed % self.short_memory_count == 0:
            self.vocabs.sort(key=lambda x: -self.get_word_fail_rate(x))
            self.short_memory.clear()
            return True
        return False

    def pick_one_word(self, idx_pre):
        """

        :param idx_pre:
        :return:
        """
        if self.mod == 'random':
            idx = random.randint(0, len(self.vocabs_index) - 1)
        elif self.mod == 'deliberate':
            self.sort_vocabs_if_needed()
            tar = random.randint(0, int(self.fail_rate_sum))
            # import pdb; pdb.set_trace()
            sum = 0
            for i in xrange(0, len(self.vocabs)):
                sum += self.get_word_fail_rate(self.vocabs[i])
                if sum >= tar and self.vocabs[i][0] not in self.short_memory:
                    return i, self.vocabs[i]
                    # else:
                    #    idx = (idx_pre + 1) % len(self.vocabs)
        return -1, self.vocabs[-1]

    def practice_one_word(self, idx_pre):
        """

        :param idx_pre:
        :return:
        """
        idx, item = self.pick_one_word(idx_pre)
        (word, showed_times, mistake_times) = item
        old_fail_rate = self.get_word_fail_rate(item)
        self.words_showed += 1

        # 读出来
        if not voice.read_one_word(word):  # 读不出就跳过
            return idx

        # 对比答案 做些存储
        try:
            user_word = raw_input()
        except KeyboardInterrupt:
            return -1
        except EOFError:  # show me the answer
            print word
            user_word = ''

        user_word = user_word.strip()
        showed_times += 1
        if user_word != word:
            mistake_times += 1
            self.words_mistype += 1
            print word + '  : ('
        else:
            self.short_memory.add(word)

        # change word record
        item = (word, showed_times, mistake_times)
        new_fail_rate = self.get_word_fail_rate(item)
        self.vocabs[idx] = item
        self.fail_rate_sum += new_fail_rate - old_fail_rate  # 修改整体的 fail rate 使得下次选单词时候更合理
        return idx

    def show_summary(self):
        """

        :return:
        """
        period = (time.time() - self.time_start) * 1.0 / 60
        msg = '''
            -------
            peroid: %0.1f min
            speed: %0.1f
            words tested: %d
            words mistype: %d
            correct rate: %0.1f%%
            -------
        ''' % (period, self.words_showed / period, self.words_showed, self.words_mistype,
               (1 - self.words_mistype * 1.0 / self.words_showed) * 100)
        print msg

    def practice(self):
        """

        :return:
        """
        idx = -1
        # 循环做练习
        while not self.is_goal_reached():
            idx = self.practice_one_word(idx)
            if idx == -1:  # means interrupted by user
                break

        # 练习结束给一个summary
        self.show_summary()

    def cal_total_fail_rate(self):
        """
        计算总的错误率
        :return:
        """
        for item in self.vocabs:  # 确保每次 都能够计算正确的 total fail rate
            self.fail_rate_sum += self.get_word_fail_rate(item)

    def add_from_file(self, filename):
        """
        从一个纯单词本中，读入所有的原始单词, 加到词表中
        :param filename: your_word_list.txt
        :return:
        """
        with open(filename) as fh:
            for word in fh.readlines():
                word = word.strip()
                self.vocabs.append((word, 0, 0))  # 默认都错一次 为了随机方便

    def reload(self, filename):
        """
        从存储中取出单词表
        :param filename: 默认存储
        :return:
        """
        if os.path.exists(filename):
            with open(filename) as fh:
                self.vocabs = json.load(fh)
                print 'successfully loaded %s' % filename
        else:
            print "can't load %s !!!" % filename
        self.filename = filename

    def dump(self):
        """
        将词表 dump 到 存储
        :return:
        """
        with open(self.filename, 'w') as fh:
            json.dump(self.vocabs, fh)


if __name__ == '__main__':

    config.prepare()

    learner = Learner('./vocab_db/vocab_db.json')
    if len(sys.argv) == 3:
        learner.reload(sys.argv[1])
        learner.add_from_file(sys.argv[2])
    elif len(sys.argv) == 2:
        learner.reload(sys.argv[1])
    elif len(sys.argv) == 1:
        learner.reload('./vocab_db/vocab_db.json')
    else:
        print 'Usage: %s [your_db.json to_add_world_list.txt]' % sys.argv[0]
        sys.exit(-1)

    learner.cal_total_fail_rate()

    learner.set_goal()

    learner.practice()

    learner.dump()
