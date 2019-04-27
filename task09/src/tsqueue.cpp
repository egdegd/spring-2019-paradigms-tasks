#include "tsqueue.h"

void threadsafe_queue_init(ThreadsafeQueue *q) {
	queue_init(&q->q);
    pthread_mutex_init(&q->mutex, nullptr);
    pthread_cond_init(&q->condition_not_empty, nullptr);
}

void threadsafe_queue_destroy(ThreadsafeQueue *q) {
    pthread_cond_destroy(&q->condition_not_empty);
    pthread_mutex_destroy(&q->mutex);
    queue_destroy(&q->q);
}

void threadsafe_queue_push(ThreadsafeQueue *q, void *data) {
    pthread_mutex_lock(&q->mutex);
    queue_push(&q->q, data);
    pthread_cond_signal(&q->condition_not_empty);
    pthread_mutex_unlock(&q->mutex);
}

void *threadsafe_queue_wait_and_pop(ThreadsafeQueue *q) {
    pthread_mutex_lock(&q->mutex);
    while (queue_empty(&q->q)) {
        pthread_cond_wait(&q->condition_not_empty, &q->mutex);
    }
    void *result = queue_pop(&q->q);
    pthread_mutex_unlock(&q->mutex);
    return result;
}
