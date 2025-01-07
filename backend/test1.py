import numpy as np

def viterbi(hidden_state,obsvation,init_prob, trans_matrix, emit_matrix):
    """
    :param init_prob:初始概率 list
    :param trans_matrix:转移概率矩阵A np.ndarray
    :param emit_matrix:发射概率矩阵B np.ndarray
    :return: 打印最佳路径
    """
    #长度为T的观测序列, 长度为N的隐状态；
    # obs_len=len(obsvation)
    # states_len=len(hidden_state)
    T = len(obsvation)
    N = len(hidden_state)

    #算法：创建一个N行T列的概率维特比路径矩阵Viterbi_matrix, 回溯路径矩阵Path_matrix
    Viterbi_matrix=np.zeros((N,T))
    Path_matrix=np.zeros((N,T))

    #算法：两个矩阵第1列的操作
    # for 每个状态  s from 1 to N do
    #      v[s, 1] = α0,s * bs(o1) // α0,s为初始概率, bs(o1)为发射概率
    #      b[s, 1] = 0

    #代码实现：两个矩阵第1列的操作：注意，代码中的第1列从0开始索引
    for s in range(N):
        Viterbi_matrix[s][0]=init_prob[s]*emit_matrix[s][0]
        Path_matrix[s][0]=0 #第1列不考虑路径的回溯，全部初始化为0

    # 算法：
    # for 每个时间  t  from 2 to T do #python代码中下标从0开始计算，这里可以改为 1~T，第1列 t=0已经处理
    # for 每个状态  s from 1 to N do // α[i, s]为转移概率
    #        v[s,t]=max(i=1...N){v[i,t-1]*Trans_matrix[i,s]*Emit_matrix[s,t]}
    #        b[s,t]=argmax(i=1...N)v[i,t-1]*Trans_matrix[i,s]#也就是取使得相乘结果最高的i，放到当前路径矩阵格子中
    # 代码实现：两个矩阵第2列~第T列的操作：
    for t in range(1,T): #第1列已经处理完，从第2列开始处理
        for s in range(N):
            max_prob=-1
            pre_max_state_index=0
            for i in range(N):
                cur_prob=Viterbi_matrix[i][t-1]*trans_matrix[i][s]*emit_matrix[s][t]
                if cur_prob>max_prob:
                    max_prob=cur_prob
                    pre_max_state_index=i
            # 记录当前节点的最大概率及回溯最优路径并分别存放在viterbi矩阵和回溯路径矩阵中
            Viterbi_matrix[s][t]=max_prob
            Path_matrix[s][t]=pre_max_state_index

    #算法：回溯
    # v[T]=max(i=1...N){v[i,T]}
    # b[T]=argmax(i=1...N)v[i,T]#使得v[i,T]最大的前一个状态索引
    #代码实现：
    print(Viterbi_matrix)
    print(Path_matrix)
    max_prob=-1
    last_state_index=0#找出观测序列最后一个状态所对应的概率最大的隐状态索引
    for s in range(N):
        if Viterbi_matrix[s][T-1]>max_prob:
            max_prob=Viterbi_matrix[s][T-1]
            last_state_index=s

    # 算法：返回从b[T] 出发的回溯路径作为最优路径。
    # 根据最后一列概率最大的隐状态索引，以及path路径矩阵往前回溯得到结果
    result=[]
    # 最后一列概率最大对应的节点词性
    result.append(hidden_state[last_state_index])
    # 接下来通过Path_matrix矩阵，从右往左回溯。
    cur_state_index=last_state_index
    for t in range(1,T):
        pre_index=int(Path_matrix[cur_state_index][T-t])
        result.append(hidden_state[pre_index])
        print(result)
        cur_state_index=pre_index

    print(result)
    final_result=""
    for t in range(0,T):
        final_result=final_result+observation[t]+"/"+result[T-t-1]+" "
    print(final_result)


# 1. 长度为3的观测序列：{dry damp soggy}
# 2. 长度为3的隐状态，sun, cloud, rain
if __name__ == '__main__':
    hidden_state = ['sun', 'cloud', 'rain']  # 隐状态
    observation = ['dry', 'damp', 'soggy']  # 观测序列
    start_probability = [0.4,0.4,0.2] # 初始概率
    # 转移概率
    trans_matrix = np.array(
        [[0.5,0.375,0.125],
         [0.25,0.125,0.625],
         [0.25,0.375,0.375]])
    # 发射概率
    emit_matrix = np.array(
        [[0.6,0.2,0.15,0.05],
         [0.25,0.25,0.25,0.25],
         [0.05,0.1,0.35,0.5]])

    viterbi(hidden_state,observation,start_probability,trans_matrix,emit_matrix)

