/* Fast annealer for pure-complete-X doom-free arrangements (Erdős #197).
   Usage: ./anneal X seed max_iters  — writes witness to stdout on success. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

static int blocklen(long v){ int k=0; long t=v-1; while(t>0){t>>=1;k++;} 
    if ((1L<<k) < v) k++; return k; }

int main(int argc, char**argv){
    long X = atol(argv[1]);
    unsigned seed = (unsigned)atoi(argv[2]);
    long long iters = atoll(argv[3]);
    srand(seed);
    /* team values */
    static long vals[3000]; int n=0;
    static int inteam[5000]; memset(inteam,0,sizeof inteam);
    for (long v=2; v<=X; v++) if (blocklen(v)%2==0){ vals[n++]=v; inteam[v]=1; }
    /* triples (x,y,z) fully in team */
    static int *trix, *triy, *triz; int nt=0, cap=2000000;
    trix=malloc(cap*4); triy=malloc(cap*4); triz=malloc(cap*4);
    for (int i=0;i<n;i++){ long y=vals[i];
        for (long d=1; y+d<=X; d++){ long x=y-d, z=y+d;
            if (x>=2 && inteam[x] && inteam[z]){
                trix[nt]=x; triy[nt]=y; triz[nt]=z; nt++; } } }
    fprintf(stderr,"n=%d triples=%d\n", n, nt);
    /* triples containing each value */
    static int *tof[5000]; static int tcnt[5000]; memset(tcnt,0,sizeof tcnt);
    for (int t=0;t<nt;t++){ tcnt[trix[t]]++; tcnt[triy[t]]++; tcnt[triz[t]]++; }
    for (int i=0;i<n;i++){ long v=vals[i]; tof[v]=malloc(tcnt[v]*4); tcnt[v]=0; }
    for (int t=0;t<nt;t++){
        tof[trix[t]][tcnt[trix[t]]++]=t;
        tof[triy[t]][tcnt[triy[t]]++]=t;
        tof[triz[t]][tcnt[triz[t]]++]=t; }
    /* position arrays */
    static int pos[5000]; static long order[3000];
    for (int i=0;i<n;i++){ order[i]=vals[i]; }
    if (argc > 4){ FILE*f=fopen(argv[4],"r"); for(int i=0;i<n;i++){ long v; fscanf(f,"%ld",&v); order[i]=v; } fclose(f); }
    else for (int i=n-1;i>0;i--){ int j=rand()%(i+1); long tmp=order[i]; order[i]=order[j]; order[j]=tmp; }
    for (int i=0;i<n;i++) pos[order[i]]=i;
    long cur=0;
    #define VIOL(t) ({ int px=pos[trix[t]], py=pos[triy[t]], pz=pos[triz[t]]; \
        ((px<py&&py<pz)||(px>py&&py>pz)) ? 1 : 0; })
    for (int t=0;t<nt;t++) cur += VIOL(t);
    fprintf(stderr,"init=%ld\n",cur);
    long best=cur;
    double T = (argc>4) ? 0.8 : 4.0;
    for (long long it=0; it<iters; it++){
        int a=rand()%n, b=rand()%n; if(a==b) continue;
        long va=order[a], vb=order[b];
        long delta=0;
        for (int q=0;q<tcnt[va];q++) delta -= VIOL(tof[va][q]);
        for (int q=0;q<tcnt[vb];q++){ int t=tof[vb][q];
            if (trix[t]!=va && triy[t]!=va && triz[t]!=va) delta -= VIOL(t); }
        pos[va]=b; pos[vb]=a; order[a]=vb; order[b]=va;
        for (int q=0;q<tcnt[va];q++) delta += VIOL(tof[va][q]);
        for (int q=0;q<tcnt[vb];q++){ int t=tof[vb][q];
            if (trix[t]!=va && triy[t]!=va && triz[t]!=va) delta += VIOL(t); }
        if (delta<=0 || (double)rand()/RAND_MAX < exp(-delta/T)) cur+=delta;
        else { pos[va]=a; pos[vb]=b; order[a]=va; order[b]=vb; }
        if (cur<best){ best=cur;
            if (best==0){
                fprintf(stderr,"FOUND at %lld\n", it);
                for (int i=0;i<n;i++) printf("%ld\n", order[i]);
                return 0; } }
        if ((it & 0xFFFFF)==0){
            T = ((argc>4)?0.8:4.0)*exp(-3.0*(double)it/iters)+0.03;
            if ((it & 0x3FFFFFF)==0)
                fprintf(stderr,"it=%lld cur=%ld best=%ld T=%.2f\n",it,cur,best,T);
        }
    }
    fprintf(stderr,"exhausted best=%ld\n",best);
    return 1;
}
