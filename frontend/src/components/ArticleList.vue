<template>
    <div v-for="article in info.results" v-bind:key="article.url" id="articles">
        <!-- 新增一个网格层 -->
        <div class="grid" :style="gridStyle(article)">
            <div class="image-container">
                <img :src="imageIfExists(article)" alt="" class="image">
            </div>
            <div>
                <div>
                    <!-- 增加了这个 span -->
                    <span v-if="article.category !== null" class="category">
                        {{ article.category.title }}
                    </span>
                    <span v-for="tag in article.tags" v-bind:key="tag" class="tag">
                        {{ tag }}
                    </span>
                </div>

                <router-link :to="{ name: 'ArticleDetail', params: { id: article.id } }" class="article-title">
                    {{ article.title }}
                </router-link>

                <div>{{ formatted_time(article.created) }}</div>
            </div>
        </div>
    </div>

    <div id="paginator">
        <span v-if="is_page_exists('previous')">
            <router-link :to="get_path('previous')">
                Prev
            </router-link>
        </span>
        <span class="current-page">
            {{ get_page_param('current') }}
        </span>
        <span v-if="is_page_exists('next')">
            <router-link :to="get_path('next')">
                Next
            </router-link>
        </span>
    </div>

</template>

<script>
// import axios from 'axios';
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import getArticleData from '@/composables/getArticleData.js'
import pagination from '@/composables/pagination.js'
import formattedTime from '@/composables/formattedTime.js'
// import { useRoute } from 'vue-router'

export default {
    name: 'ArticleList',
    // 组合式 APi 入口,Vue 执行 setup() 的时机非常早，此时 Vue 的实例都尚未生成，因此在 setup 中没有 this。这意味着除了 props 之外，你将无法访问组件中的任何属性：比如数据、计算属性或方法。
    setup() {
        // 你不能普通的如 let info = '' 这样声明状态，这不是响应式的，而只是个普通的字符串。因此用 Vue 3 提供的 ref 将其包装成一个响应式的对象，和旧的 data 中的数据一样。
        // 用 return 将状态数据返回，Vue 就会将其注入到 Vue 实例的 this 中。
        const info = ref('');
        // const route = useRoute();
        const route = useRoute();
        const {
            is_page_exists,
            get_page_param,
            get_path
        } = pagination(info, route);
        // 日期格式化
        const formatted_time = formattedTime;
        // 创建路由
        // const route = useRoute();
        // 获取文章列表数据的方法
        // 新增响应式对象
        const kwargs = ref({ page: 0, searchText: '' });
        // 修改方法，把此对象作为第三个参数
        getArticleData(info, route, kwargs);
        return {
            info,
            is_page_exists,
            get_page_param,
            get_path,
            formatted_time,
            // get_article_data,
        }
    },
    methods: {
        imageIfExists(article) {
            if (article.avatar) {
                return article.avatar.content
            }
        },
        gridStyle(article) {
            if (article.avatar) {
                return {
                    display: 'grid',
                    gridTemplateColumns: '1fr 4fr'
                }
            }
        },
        formatted_time: function (iso_date_string) {
            const date = new Date(iso_date_string);
            return date.toLocaleDateString()
        },
    },
}


</script>

<!-- "scoped" 使样式仅在当前组件生效 -->
<style scoped>
.image {
    width: 180px;
    border-radius: 10px;
    box-shadow: darkslategrey 0 0 12px;
}

.image-container {
    width: 200px;
}

.grid {
    padding-bottom: 10px;
}

.category {
    padding: 5px 10px 5px 10px;
    margin: 5px 5px 5px 0;
    font-family: Georgia, Arial, sans-serif;
    font-size: small;
    background-color: darkred;
    color: whitesmoke;
    border-radius: 15px;
}


#articles {
    padding: 10px;
}

.article-title {
    font-size: large;
    font-weight: bolder;
    color: black;
    text-decoration: none;
    padding: 5px 0 5px 0;
}

.tag {
    padding: 2px 5px 2px 5px;
    margin: 5px 5px 5px 0;
    font-family: Georgia, Arial, sans-serif;
    font-size: small;
    background-color: #4e4e4e;
    color: whitesmoke;
    border-radius: 5px;
}

#paginator {
    text-align: center;
    padding-top: 50px;
}

a {
    color: black;
}

.current-page {
    font-size: x-large;
    font-weight: bold;
    padding-left: 10px;
    padding-right: 10px;
}
</style>